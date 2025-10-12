import os
import base64
from io import BytesIO
from PIL import Image
from typing import Dict, Any
import time

# ==============================================================================
# Configuration
# ==============================================================================

# Local cartoon image folder path
IMAGE_FOLDER = "./fish/fish_ic"

# ==============================================================================
# Core Functions
# ==============================================================================

def load_local_cartoon_image(species_en: str, image_folder: str = None) -> Dict[str, Any]:
    """
    Load pre-generated cartoon image from local folder
    
    Args:
        species_en (str): English name of the fish species
        image_folder (str, optional): Image folder path. Defaults to IMAGE_FOLDER
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success (bool): Whether the image was loaded successfully
            - cartoon_image (str): Base64 encoded image (if success=True)
            - image_path (str): Image file path (if success=True)
            - error (str): Error message (if success=False)
    
    Example:
        >>> result = load_local_cartoon_image("Southern Fiddler Ray (Banjo)")
        >>> if result["success"]:
        ...     image_data = result["cartoon_image"]
    """
    if image_folder is None:
        image_folder = IMAGE_FOLDER
    
    try:
        # Construct local image path
        local_image_path = os.path.join(image_folder, f"{species_en}.png")
        
        print(f"   - Attempting to load image from: {local_image_path}")
        
        # Check if file exists
        if not os.path.exists(local_image_path):
            error_msg = (
                f"Image file not found! Please check:\n"
                f"   1. Does the folder '{image_folder}' exist?\n"
                f"   2. Does the file '{species_en}.png' exist in the folder?\n"
                f"   3. Check for spaces and case sensitivity in the filename"
            )
            print(f"Error: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
        
        # Load image
        img = Image.open(local_image_path)
        print(f"Image loaded successfully!")
        
        # Convert to Base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {
            "success": True,
            "cartoon_image": f"data:image/png;base64,{base64_string}",
            "image_path": local_image_path
        }
        
    except Exception as e:
        error_msg = f"Error loading image: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "success": False,
            "error": error_msg
        }


def process_avatar(species_en: str = None, image_folder: str = None) -> Dict[str, Any]:
    """
    Process avatar request and return cartoon image
    
    Main API interface function for avatar conversion requests.
    
    Args:
        species_en (str, optional): English name of the fish species. 
                                   If None, uses default test image.
        image_folder (str, optional): Image folder path. Defaults to IMAGE_FOLDER
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success (bool): Whether conversion was successful
            - cartoon_image (str): Base64 encoded cartoon image (if success=True)
            - processing_time (float): Processing time in seconds (if success=True)
            - image_path (str): Image path (if success=True)
            - error (str): Error message (if success=False)
    
    Example:
        >>> result = process_avatar("Southern Fiddler Ray (Banjo)")
        >>> if result["success"]:
        ...     print(f"Processing time: {result['processing_time']}s")
        ...     image_data = result["cartoon_image"]
        >>> else:
        ...     print(f"Error: {result['error']}")
    """
    start_time = time.time()
    
    if species_en is None:
        # Use default test species
        species_en = "Southern Fiddler Ray (Banjo)"
    
    print(f"\n--- Processing avatar for species: {species_en} ---")
    
    try:
        # Load local cartoon image
        result = load_local_cartoon_image(species_en, image_folder)
        
        if result["success"]:
            elapsed_time = time.time() - start_time
            print(f"Avatar processing successful! ({elapsed_time:.2f}s)")
            print(f"Base64 length: {len(result['cartoon_image'])} bytes")
            
            return {
                "success": True,
                "cartoon_image": result["cartoon_image"],
                "image_path": result["image_path"],
                "processing_time": round(elapsed_time, 2)
            }
        else:
            elapsed_time = time.time() - start_time
            print(f"Avatar processing failed ({elapsed_time:.2f}s)")
            return {
                "success": False,
                "error": result["error"],
                "processing_time": round(elapsed_time, 2)
            }
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = f"Unexpected error during processing: {str(e)}"
        print(f"Error: {error_msg} ({elapsed_time:.2f}s)")
        return {
            "success": False,
            "error": error_msg,
            "processing_time": round(elapsed_time, 2)
        }


# ==============================================================================
# Test Functions
# ==============================================================================

def test_process_avatar():
    """Test process_avatar function"""
    print("\n=== Testing process_avatar function ===\n")
    
    # Test species
    test_species = "Southern Fiddler Ray (Banjo)"
    
    result = process_avatar(test_species)
    
    if result["success"]:
        print(f"\nTest successful!")
        print(f"   Processing time: {result['processing_time']}s")
        print(f"   Image path: {result['image_path']}")
        print(f"   Base64 length: {len(result['cartoon_image'])} bytes")
        
        # Try to display image in Jupyter environment
        try:
            from IPython.display import Image as IImage, display
            display(IImage(data=base64.b64decode(result['cartoon_image'].split(',')[1])))
        except ImportError:
            print("   (Not in Jupyter environment, cannot display image directly)")
    else:
        print(f"\nTest failed!")
        print(f"   Error: {result['error']}")


if __name__ == "__main__":
    # Run test
    test_process_avatar()


