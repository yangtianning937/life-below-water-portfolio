import requests
import random
import json
import torch
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO
import base64

# Make sure model.py file is uploaded to the correct directory
from recommend.model import Generator

# Configuration
# Replace with actual Google API Key
GOOGLE_API_KEY = "AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg"

# paprika.py is the model weight path
# Make sure paprika.pt file is uploaded to the correct directory
MODEL_PATH = "./recommend/fav2.pt"


# AniGAN model loading and transformation function
def load_and_transform_with_animeganv2(image_urls):
    """
    Download images from URL, load the model, and perform style transfer.

    Args:
        image_urls (list): List of Google API image URLs.

    Returns:
        list: List of base64-encoded transformed images.
    """
    # Ensure GPU is available
    if torch.cuda.is_available():
        print("GPU is available. Activating.")
    else:
        print("GPU is not available. Using CPU.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load pre-trained AniGAN model (using imported Generator class)
    try:
        # Fix: remove init parameters. This version of Generator class doesn’t need any parameters.
        model = Generator().to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()  # Set to evaluation mode
        print("AniGANv2 model loaded successfully.")
    except Exception as e:
        print(f"Error loading AniGANv2 model: {e}")
        return [f"Error loading model: {e}"] * len(image_urls)

    # Define image preprocessing pipeline (based on AniGAN official example)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    # Define postprocessing pipeline (convert from -1~1 back to 0~1, then to PIL Image)
    to_pil_image = transforms.ToPILImage()

    ghibli_photos_base64 = []

    for url in image_urls:
        try:
            # 1. Download image
            print(f"Downloading image from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()  # Ensure request successful
            img = Image.open(BytesIO(response.content)).convert("RGB")

            # 2. Resize image to fit model input (AniGAN usually expects 512x512)
            img_resized = img.resize((512, 512), Image.LANCZOS)

            # 3. Preprocess and convert to tensor
            img_tensor = transform(img_resized).unsqueeze(0).to(device)

            # 4. Perform style transfer
            with torch.no_grad():  # Disable gradient calc during inference to save memory and time
                output_tensor = model(img_tensor)

            # 5. Postprocess: convert from [-1, 1] range back to [0, 1]
            output_tensor = (output_tensor + 1) / 2

            # 6. Convert tensor back to PIL image
            output_img = to_pil_image(output_tensor.squeeze(0).cpu())

            # 7. Save transformed image to memory and encode in base64
            buffered = BytesIO()
            output_img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            ghibli_photos_base64.append(f"data:image/png;base64,{img_base64}")

        except Exception as e:
            print(f"Error processing image from URL {url}: {e}")
            ghibli_photos_base64.append(f"Error processing image: {e}")

    return ghibli_photos_base64


# Other code remains the same

# Google Places API (same as previous code)
def get_place_details(place_id, fields):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": fields,
        "key": GOOGLE_API_KEY
    }
    r = requests.get(details_url, params=params)
    r.raise_for_status()
    return r.json().get("result", {})


def search_nearby_places(lat, lon, keyword, radius=50000, min_rating=4.0):
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": keyword,
        "key": GOOGLE_API_KEY
    }
    r = requests.get(search_url, params=params)
    r.raise_for_status()
    results = r.json().get("results", [])
    filtered_results = [
        res for res in results if res.get("rating", 0) >= min_rating
    ]
    return filtered_results


def get_beach_info_and_photos(lat, lon, radius=500000, max_photos=3):
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "keyword": "beach",
        "key": GOOGLE_API_KEY
    }
    r = requests.get(search_url, params=params)
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
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo?"
            f"maxwidth=800&photoreference={ref}&key={GOOGLE_API_KEY}"
        )
        photo_urls.append(photo_url)

    return {
        "beach_name": details.get("name"),
        "lat": details["geometry"]["location"]["lat"],
        "lon": details["geometry"]["location"]["lng"],
        "photos": photo_urls
    }


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


# Get nearby recommendations (same as previous code)
def get_nearby_recommendations(lat, lon):
    recommendations = {}

    activities = search_nearby_places(lat, lon, keyword="surf school|kayak rental|paddle board rental", min_rating=4.0)
    recommendations["activities"] = [
        {"name": res["name"], "rating": res.get("rating")} for res in activities[:3]
    ]

    attractions = search_nearby_places(lat, lon, keyword="attraction|park|lookout|sightseeing", min_rating=4.2)
    recommendations["attractions"] = [
        {"name": res["name"], "rating": res.get("rating")} for res in attractions[:3]
    ]

    restaurants = search_nearby_places(lat, lon, keyword="restaurant", min_rating=4.4)
    restaurants.sort(key=lambda x: x.get("rating", 0), reverse=True)
    recommendations["restaurants"] = [
        {"name": res["name"], "rating": res.get("rating"), "address": res.get("vicinity")}
        for res in restaurants[:4]
    ]

    return recommendations


# Main process
def analyze_nearby_beaches(lat, lon, radius_m=500000):
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