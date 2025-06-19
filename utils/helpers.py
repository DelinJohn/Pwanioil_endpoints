import base64
from io import BytesIO
import time
from functools import wraps
import re


def base64_to_image(img):
    image_bytes = base64.b64decode(img.data[0].b64_json)
    image_io = BytesIO(image_bytes)
    return image_io




def normalize_output_type(text: str) -> str:
    """
    Normalize output type to one of: 'image', 'text', 'image_and_text'.
    """
    text = text.lower()

    has_image = re.search(r'\bimage\b', text)
    has_text = re.search(r'\btext\b', text)

    if has_image and has_text:
        return "image_and_text"
    elif has_image:
        return "image"
    elif has_text:
        return "text"
    else:
        return "unknown"
    

