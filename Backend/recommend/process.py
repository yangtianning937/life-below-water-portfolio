import requests
import random
import json
import torch
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
import hashlib
from functools import lru_cache
import time

# Make sure model.py file is uploaded to the correct directory
from recommend.model import Generator

# Configuration
# Replace with actual Google API Key
GOOGLE_API_KEY = "AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg"

# paprika.py is the model weight path
# Make sure paprika.pt file is uploaded to the correct directory
MODEL_PATH = "./recommend/fav2.pt"

# Global model cache to avoid reloading
_MODEL_CACHE = {"model": None, "device": None}

# Global requests session for connection pooling
_SESSION = requests.Session()
_SESSION.headers.update({'User-Agent': 'Mozilla/5.0'})

# Image processing cache - stores processed images by URL hash
# LRU cache with max 100 items to prevent memory issues
_IMAGE_CACHE = {}
_IMAGE_CACHE_MAX_SIZE = 100
_IMAGE_CACHE_EXPIRY = 3600 * 24 * 7  # 7 days

# API response cache with expiry
_API_CACHE = {}
_API_CACHE_EXPIRY = 3600 * 24 * 7  # 7 days for API responses


def _get_cache_key(data):
    """Generate cache key from data."""
    if isinstance(data, str):
        return hashlib.md5(data.encode()).hexdigest()
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()


def _clean_cache(cache_dict, max_size, expiry):
    """Remove expired and excess cache entries."""
    current_time = time.time()
    # Remove expired entries (older than 7 days)
    expired_keys = [k for k, v in cache_dict.items() if current_time - v.get('timestamp', 0) > expiry]
    if expired_keys:
        print(f"Cleaning {len(expired_keys)} expired cache entries (older than {expiry/86400:.1f} days)")
    for k in expired_keys:
        del cache_dict[k]
    
    # If still too large, remove oldest entries
    if len(cache_dict) > max_size:
        excess = len(cache_dict) - max_size
        sorted_items = sorted(cache_dict.items(), key=lambda x: x[1].get('timestamp', 0))
        print(f"Cleaning {excess} excess cache entries (max size: {max_size})")
        for k, _ in sorted_items[:excess]:
            del cache_dict[k]


def get_cache_stats():
    """Get current cache statistics for monitoring."""
    current_time = time.time()
    
    # Image cache stats
    img_total = len(_IMAGE_CACHE)
    img_expired = sum(1 for v in _IMAGE_CACHE.values() 
                      if current_time - v.get('timestamp', 0) > _IMAGE_CACHE_EXPIRY)
    
    # API cache stats
    api_total = len(_API_CACHE)
    api_expired = sum(1 for v in _API_CACHE.values() 
                      if current_time - v.get('timestamp', 0) > _API_CACHE_EXPIRY)
    
    return {
        "image_cache": {
            "total": img_total,
            "expired": img_expired,
            "active": img_total - img_expired,
            "max_size": _IMAGE_CACHE_MAX_SIZE,
            "expiry_days": _IMAGE_CACHE_EXPIRY / 86400
        },
        "api_cache": {
            "total": api_total,
            "expired": api_expired,
            "active": api_total - api_expired,
            "expiry_days": _API_CACHE_EXPIRY / 86400
        }
    }


def clear_all_caches():
    """Manually clear all caches. Useful for testing or maintenance."""
    _IMAGE_CACHE.clear()
    _API_CACHE.clear()
    print("All caches cleared")


def get_model():
    """Get or create cached model instance."""
    if _MODEL_CACHE["model"] is None:
        if torch.cuda.is_available():
            print("GPU is available. Activating.")
        else:
            print("GPU is not available. Using CPU.")
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        try:
            model = Generator().to(device)
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
            model.eval()
            _MODEL_CACHE["model"] = model
            _MODEL_CACHE["device"] = device
            print("AniGANv2 model loaded successfully and cached.")
        except Exception as e:
            print(f"Error loading AniGANv2 model: {e}")
            raise
    
    return _MODEL_CACHE["model"], _MODEL_CACHE["device"]


def download_image(url, timeout=5):
    """Download a single image with shorter timeout using session for connection pooling."""
    try:
        print(f"Downloading image from URL: {url}")
        response = _SESSION.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        # Use stream to start processing earlier
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img, None
    except Exception as e:
        print(f"Error downloading image from URL {url}: {e}")
        return None, e


# AniGAN model loading and transformation function
def load_and_transform_with_animeganv2(image_urls):
    """
    Download images from URL in parallel, load the model, and perform style transfer.
    Uses caching to avoid reprocessing the same images.

    Args:
        image_urls (list): List of Google API image URLs.

    Returns:
        list: List of base64-encoded transformed images.
    """
    if not image_urls:
        return []
    
    # Clean image cache periodically
    _clean_cache(_IMAGE_CACHE, _IMAGE_CACHE_MAX_SIZE, _IMAGE_CACHE_EXPIRY)
    
    # Check cache first
    cached_results = []
    urls_to_process = []
    url_indices = []
    
    current_time = time.time()
    for idx, url in enumerate(image_urls):
        cache_key = _get_cache_key(url)
        if cache_key in _IMAGE_CACHE:
            # 检查是否过期（超过7天）
            if current_time - _IMAGE_CACHE[cache_key]['timestamp'] <= _IMAGE_CACHE_EXPIRY:
                cached_results.append((idx, _IMAGE_CACHE[cache_key]['data']))
                print(f"Cache HIT for image {idx}")
            else:
                # 过期了，需要重新处理
                del _IMAGE_CACHE[cache_key]
                urls_to_process.append(url)
                url_indices.append(idx)
                print(f"Cache EXPIRED for image {idx}, will reprocess")
        else:
            urls_to_process.append(url)
            url_indices.append(idx)
            print(f"Cache MISS for image {idx}")
    
    # If all cached, return immediately
    if not urls_to_process:
        print(f"All {len(image_urls)} images served from cache!")
        result = [None] * len(image_urls)
        for idx, data in cached_results:
            result[idx] = data
        return result
    
    print(f"Processing {len(urls_to_process)} new images, {len(cached_results)} from cache")
    
    # Get cached model
    try:
        model, device = get_model()
    except Exception as e:
        return [f"Error loading model: {e}"] * len(image_urls)

    # Define image preprocessing pipeline (based on AniGAN official example)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    # Define postprocessing pipeline (convert from -1~1 back to 0~1, then to PIL Image)
    to_pil_image = transforms.ToPILImage()

    # Step 1: Download only uncached images in parallel
    print(f"Starting parallel download of {len(urls_to_process)} images...")
    downloaded_images = []
    with ThreadPoolExecutor(max_workers=min(len(urls_to_process), 10)) as executor:
        future_to_url = {executor.submit(download_image, url): url for url in urls_to_process}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            img, error = future.result()
            downloaded_images.append((url, img, error))
    
    print(f"Downloaded {sum(1 for _, img, _ in downloaded_images if img is not None)} images successfully.")

    # Step 2: Prepare all valid images for batch processing
    valid_images = []
    processing_indices = []
    processing_urls = []
    new_results = [None] * len(urls_to_process)
    
    for idx, (url, img, error) in enumerate(downloaded_images):
        if error or img is None:
            new_results[idx] = f"Error downloading image: {error}"
        else:
            # Resize image to fit model input (smaller size for faster processing)
            img_resized = img.resize((512, 512), Image.LANCZOS)
            valid_images.append(img_resized)
            processing_indices.append(idx)
            processing_urls.append(url)
    
    # Step 3: Batch process all valid images on GPU
    if valid_images:
        try:
            # Convert all images to tensors
            img_tensors = torch.stack([transform(img) for img in valid_images]).to(device)
            
            # Use half precision (FP16) if GPU is available for faster inference
            if torch.cuda.is_available():
                model_fp16 = model.half()
                img_tensors = img_tensors.half()
            else:
                model_fp16 = model
            
            # Batch inference - process all images at once
            with torch.no_grad():
                output_tensors = model_fp16(img_tensors)
            
            # Postprocess all outputs
            output_tensors = (output_tensors.float() + 1) / 2
            
            # Convert each output to base64 and cache it
            for i, output_tensor in enumerate(output_tensors):
                try:
                    output_img = to_pil_image(output_tensor.cpu())
                    buffered = BytesIO()
                    # Use JPEG with lower quality - much smaller and faster
                    output_img.save(buffered, format="JPEG", quality=70, optimize=True)
                    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    result_data = f"data:image/jpeg;base64,{img_base64}"
                    
                    # Store in results
                    new_results[processing_indices[i]] = result_data
                    
                    # Cache the result
                    cache_key = _get_cache_key(processing_urls[i])
                    _IMAGE_CACHE[cache_key] = {
                        'data': result_data,
                        'timestamp': time.time()
                    }
                    print(f"Cached processed image {i}")
                    
                except Exception as e:
                    print(f"Error encoding image {i}: {e}")
                    new_results[processing_indices[i]] = f"Error encoding image: {e}"
                    
        except Exception as e:
            print(f"Error in batch processing: {e}")
            # Fallback: mark all as errors
            for idx in processing_indices:
                if new_results[idx] is None:
                    new_results[idx] = f"Error processing image: {e}"

    # Step 4: Merge cached and newly processed results
    final_results = [None] * len(image_urls)
    
    # Add cached results
    for idx, data in cached_results:
        final_results[idx] = data
    
    # Add newly processed results
    for i, url_idx in enumerate(url_indices):
        final_results[url_idx] = new_results[i]
    
    return final_results


# Other code remains the same

# Google Places API with session and shorter timeout
def get_place_details(place_id, fields, timeout=5):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": fields,
        "key": GOOGLE_API_KEY
    }
    r = _SESSION.get(details_url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json().get("result", {})


def search_nearby_places(lat, lon, keyword, radius=50000, min_rating=4.0, timeout=5):
    # Check cache first
    cache_key = _get_cache_key({
        'type': 'search_nearby',
        'lat': round(lat, 4),  # Round to reduce cache misses
        'lon': round(lon, 4),
        'keyword': keyword,
        'radius': radius,
        'min_rating': min_rating
    })
    
    if cache_key in _API_CACHE:
        cache_entry = _API_CACHE[cache_key]
        if time.time() - cache_entry['timestamp'] < _API_CACHE_EXPIRY:
            print(f"API Cache HIT for search_nearby_places: {keyword}")
            return cache_entry['data']
    
    # Make API call
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": keyword,
        "key": GOOGLE_API_KEY
    }
    r = _SESSION.get(search_url, params=params, timeout=timeout)
    r.raise_for_status()
    results = r.json().get("results", [])
    filtered_results = [
        res for res in results if res.get("rating", 0) >= min_rating
    ]
    
    # Cache the result
    _API_CACHE[cache_key] = {
        'data': filtered_results,
        'timestamp': time.time()
    }
    print(f"API Cache MISS for search_nearby_places: {keyword}")
    
    return filtered_results


def get_beach_info_and_photos(lat, lon, radius=500000, max_photos=3, timeout=5):
    # Check cache first
    cache_key = _get_cache_key({
        'type': 'beach_info',
        'lat': round(lat, 4),
        'lon': round(lon, 4),
        'radius': radius,
        'max_photos': max_photos
    })
    
    if cache_key in _API_CACHE:
        cache_entry = _API_CACHE[cache_key]
        if time.time() - cache_entry['timestamp'] < _API_CACHE_EXPIRY:
            print(f"API Cache HIT for get_beach_info_and_photos")
            return cache_entry['data']
    
    # Make API call
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": "beach",
        "key": GOOGLE_API_KEY
    }
    r = _SESSION.get(search_url, params=params, timeout=timeout)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return None

    place_id = results[0]["place_id"]
    details = get_place_details(place_id, "name,geometry,photos")

    photos = details.get("photos", [])
    photo_urls = []
    for p in photos[:max_photos]:
        ref = p["photo_reference"]
        # Reduced image size to 400 for faster download (will resize to 512 anyway)
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo?"
            f"maxwidth=400&photoreference={ref}&key={GOOGLE_API_KEY}"
        )
        photo_urls.append(photo_url)

    result = {
        "beach_name": details.get("name"),
        "lat": details["geometry"]["location"]["lat"],
        "lon": details["geometry"]["location"]["lng"],
        "photos": photo_urls
    }
    
    # Cache the result
    _API_CACHE[cache_key] = {
        'data': result,
        'timestamp': time.time()
    }
    print(f"API Cache MISS for get_beach_info_and_photos")
    
    return result


# Water quality recommendation logic (same as previous code)
def assess_beach_water_quality():
    water_quality = {
        "clarity": random.uniform(0, 1),
        "pollution": random.uniform(0, 1),
        "fish_stock": random.uniform(0, 1),
    }

    recommendations = []
    if water_quality["clarity"] > 0.6 and water_quality["pollution"] < 0.3:
        recommendations.append("😊 Suitable for diving: clear water, high visibility.")
    else:
        recommendations.append("☹️ Not very suitable for diving: visibility or water quality not ideal.")

    if water_quality["pollution"] < 0.4:
        recommendations.append("🎉 Suitable for swimming: low pollution, safe water quality.")
    else:
        recommendations.append("😫 Swimming not recommended: high pollution level.")

    if 0.3 < water_quality["fish_stock"] < 0.7:
        recommendations.append("‼️ Fishing possible, but pay attention to ecological protection and avoid overfishing.")
    elif water_quality["fish_stock"] >= 0.7:
        recommendations.append("🎆 Rich fish resources, suitable for fishing.")
    else:
        recommendations.append("🙅 Few fish, fishing not recommended to protect the ecosystem.")

    return {
        "water_quality": water_quality,
        "recommendations": recommendations
    }


# Get nearby recommendations with parallel API calls
def get_nearby_recommendations(lat, lon):
    recommendations = {}

    # Parallel API calls for different categories
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all API calls at once
        future_activities = executor.submit(
            search_nearby_places, lat, lon, 
            keyword="surf school|kayak rental|paddle board rental", min_rating=4.0
        )
        future_attractions = executor.submit(
            search_nearby_places, lat, lon,
            keyword="attraction|park|lookout|sightseeing", min_rating=4.2
        )
        future_restaurants = executor.submit(
            search_nearby_places, lat, lon,
            keyword="restaurant", min_rating=4.4
        )
        
        # Collect results
        activities = future_activities.result()
        recommendations["activities"] = [
            {"name": res["name"], "rating": res.get("rating")} for res in activities[:3]
        ]

        attractions = future_attractions.result()
        recommendations["attractions"] = [
            {"name": res["name"], "rating": res.get("rating")} for res in attractions[:3]
        ]

        restaurants = future_restaurants.result()
        restaurants.sort(key=lambda x: x.get("rating", 0), reverse=True)
        recommendations["restaurants"] = [
            {"name": res["name"], "rating": res.get("rating"), "address": res.get("vicinity")}
            for res in restaurants[:4]
        ]

    return recommendations


# Main process
def analyze_nearby_beaches(lat, lon, radius_m=500000):
    # Clean API cache periodically
    _clean_cache(_API_CACHE, 200, _API_CACHE_EXPIRY)
    
    beaches = []
    beach_data = get_beach_info_and_photos(lat, lon, radius=radius_m)

    if beach_data:
        ghibli_photos_base64 = load_and_transform_with_animeganv2(beach_data["photos"])
        water_eval = assess_beach_water_quality()
        nearby_recommendations = get_nearby_recommendations(lat, lon)

        beaches.append({
            "name": beach_data["beach_name"],
            "location": {"lat": beach_data["lat"], "lon": beach_data["lon"]},
            "photos": ghibli_photos_base64,
            "assessment": water_eval,
            "recommendations": nearby_recommendations
        })

    return beaches