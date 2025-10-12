import torch
from torch import nn
import torch.nn.functional as F
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import os
from typing import Dict, Any, List

# ==============================================================================
# Step 1: Model Architecture Definition
# ==============================================================================

class ConvNormLReLU(nn.Sequential):
    def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1, pad_mode="reflect", groups=1, bias=False):

        pad_layer = {
            "zero":    nn.ZeroPad2d,
            "same":    nn.ReplicationPad2d,
            "reflect": nn.ReflectionPad2d,
        }
        if pad_mode not in pad_layer:
            raise NotImplementedError

        super(ConvNormLReLU, self).__init__(
            pad_layer[pad_mode](padding),
            nn.Conv2d(in_ch, out_ch, kernel_size=kernel_size, stride=stride, padding=0, groups=groups, bias=bias),
            nn.GroupNorm(num_groups=1, num_channels=out_ch, affine=True),
            nn.LeakyReLU(0.2, inplace=True)
        )


class InvertedResBlock(nn.Module):
    def __init__(self, in_ch, out_ch, expansion_ratio=2):
        super(InvertedResBlock, self).__init__()

        self.use_res_connect = in_ch == out_ch
        bottleneck = int(round(in_ch*expansion_ratio))
        layers = []
        # Expansion convolution (point-wise 1x1)
        if expansion_ratio != 1:
            layers.append(ConvNormLReLU(in_ch, bottleneck, kernel_size=1, padding=0))

        # Depth-wise convolution
        layers.append(ConvNormLReLU(bottleneck, bottleneck, groups=bottleneck, bias=True))
        # Projection convolution (point-wise 1x1)
        layers.append(nn.Conv2d(bottleneck, out_ch, kernel_size=1, padding=0, bias=False))
        layers.append(nn.GroupNorm(num_groups=1, num_channels=out_ch, affine=True))

        self.layers = nn.Sequential(*layers)

    def forward(self, input):
        out = self.layers(input)
        if self.use_res_connect:
            out = input + out
        return out


class Generator(nn.Module):
    def __init__(self, ):
        super().__init__()

        self.block_a = nn.Sequential(
            ConvNormLReLU(3,  32, kernel_size=7, padding=3),
            ConvNormLReLU(32, 64, stride=2, padding=(0,1,0,1)),
            ConvNormLReLU(64, 64)
        )

        self.block_b = nn.Sequential(
            ConvNormLReLU(64,  128, stride=2, padding=(0,1,0,1)),
            ConvNormLReLU(128, 128)
        )

        self.block_c = nn.Sequential(
            ConvNormLReLU(128, 128),
            InvertedResBlock(128, 256, 2),
            InvertedResBlock(256, 256, 2),
            InvertedResBlock(256, 256, 2),
            InvertedResBlock(256, 256, 2),
            ConvNormLReLU(256, 128),
        )

        self.block_d = nn.Sequential(
            ConvNormLReLU(128, 128),
            ConvNormLReLU(128, 128)
        )

        self.block_e = nn.Sequential(
            ConvNormLReLU(128, 64),
            ConvNormLReLU(64,  64),
            ConvNormLReLU(64,  32, kernel_size=7, padding=3)
        )

        self.out_layer = nn.Sequential(
            nn.Conv2d(32, 3, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Tanh()
        )

    def forward(self, input, align_corners=True):
        out = self.block_a(input)
        half_size = out.size()[-2:]
        out = self.block_b(out)
        out = self.block_c(out)

        if align_corners:
            out = F.interpolate(out, half_size, mode="bilinear", align_corners=True)
        else:
            out = F.interpolate(out, scale_factor=2, mode="bilinear", align_corners=False)
        out = self.block_d(out)

        if align_corners:
            out = F.interpolate(out, input.size()[-2:], mode="bilinear", align_corners=True)
        else:
            out = F.interpolate(out, scale_factor=2, mode="bilinear", align_corners=False)
        out = self.block_e(out)

        out = self.out_layer(out)
        return out


# ==============================================================================
# Step 2: Core Conversion Function
# ==============================================================================

## Generator class definition remains unchanged

MODEL_WEIGHTS_PATH = "./fish/fne.pt" # Modify this path as needed

def convert_url_to_base64_cartoon(image_url: str) -> str:
    """
    Downloads the image, performs PyTorch model inference for style transfer,
    and encodes the resulting image as a Base64 string (Data URI format).

    Args:
        image_url: The URL of the image (e.g., from Wikipedia).

    Returns:
        The converted image's Base64 encoded string (Data URI format),
        or an ERROR string if conversion fails.
    """

    # 1. Set up device and load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device used: {device}")

    try:
        model = Generator().to(device)
        model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH, map_location=device))
        model.eval()
        print(f"✅ Model {MODEL_WEIGHTS_PATH} loaded successfully.")
    except FileNotFoundError:
        return f"ERROR: Model weights file not found. Please confirm the filename is {MODEL_WEIGHTS_PATH} or modify the path."
    except Exception as e:
        return f"ERROR: Failed to load model or weights: {e}"

    # 2. Corrected image download and preprocessing
    try:
        # Add User-Agent header to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(image_url, headers=headers, timeout=5)
        # Check HTTP status code, throws an exception if not 200
        response.raise_for_status()

        # Read the image using PIL
        img_data = BytesIO(response.content)
        img = Image.open(img_data).convert("RGB")

        # Convert to Tensor: [H, W, C] -> [C, H, W]
        img_np = np.array(img).astype(np.float32)
        input_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0)

        # Normalize to [-1, 1]
        input_tensor = (input_tensor / 127.5) - 1.0
        input_tensor = input_tensor.to(device)

    except requests.exceptions.RequestException as e:
        # If download fails again, a new error message will be displayed, e.g., 404 or other network issues
        return f"ERROR: Failed to download image: {e}"
    except Exception as e:
        return f"ERROR: Failed to preprocess image: {e}"

    # 3. Run inference (unchanged)
    try:
        with torch.no_grad():
            output_tensor = model(input_tensor)

        # 4. Post-processing (unchanged)
        output_tensor = (output_tensor + 1.0) * 127.5
        output_np = output_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy().astype(np.uint8)

        cartoon_img = Image.fromarray(output_np)

        # 5. Encode to Base64 (unchanged)
        buffered = BytesIO()
        cartoon_img.save(buffered, format="PNG")
        base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{base64_string}"

    except Exception as e:
        return f"ERROR: Inference or encoding failed: {e}"


# ==============================================================================
# Step 4: Process Avatar for API
# ==============================================================================

def process_avatar(image_url: str = None) -> Dict[str, Any]:
    """
    Process image conversion request and return cartoonized image
    
    Args:
        image_url: Image URL address
        
    Returns:
        Dictionary containing cartoon image base64 encoding, or error message
    """
    import time
    start_time = time.time()
    
    if not image_url:
        # Default test image
        image_url = "https://upload.wikimedia.org/wikipedia/commons/1/10/Trygonorrhina_sp.jpg"
    
    print(f"\n--- Generating cartoon for URL: {image_url} ---")
    
    try:
        base64_cartoon_image = convert_url_to_base64_cartoon(image_url)
        
        if base64_cartoon_image.startswith("ERROR:"):
            print(f"❌ Error: {base64_cartoon_image}")
            return {
                "success": False,
                "error": base64_cartoon_image.replace("ERROR: ", "")
            }
        else:
            elapsed_time = time.time() - start_time
            print(f"✅ Style transfer successful! ({elapsed_time:.2f}s)")
            print(f"📊 Base64 Data URI string length: {len(base64_cartoon_image)} bytes")
            return {
                "success": True,
                "cartoon_image": base64_cartoon_image,
                "processing_time": round(elapsed_time, 2)
            }
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = f"Unexpected error during processing: {str(e)}"
        print(f"❌ {error_msg} ({elapsed_time:.2f}s)")
        return {
            "success": False,
            "error": error_msg
        }


# ==============================================================================
# Step 5: Test Function (Optional)
# ==============================================================================

def test_process_avatar():
    """Test function"""
    # Example Wikipedia image URL for Banded Stingaree
    WIKIPEDIA_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/1/10/Trygonorrhina_sp.jpg"

    print(f"\n--- Testing with URL: {WIKIPEDIA_IMAGE_URL} ---")

    result = process_avatar(WIKIPEDIA_IMAGE_URL)

    if result.get("success"):
        base64_cartoon_image = result["cartoon_image"]
        print("\nStyle transfer successful! Base64 encoded cartoon image generated.")
        print(f"Base64 Data URI string length: {len(base64_cartoon_image)} bytes")

        # Display image directly in Colab (requires importing IPython.display)
        try:
            from IPython.display import Image as IImage, display
            display(IImage(data=base64.b64decode(base64_cartoon_image.split(',')[1])))
        except ImportError:
            print("\nHint: Unable to import IPython.display. Please manually execute the following code in Colab to display the image:")
            print(f"from IPython.display import HTML\nHTML(f'<img src=\"{base64_cartoon_image}\">')")
    else:
        print(f"Error: {result.get('error')}")
