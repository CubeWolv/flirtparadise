from django import template
from PIL import Image
import os
from django.conf import settings

register = template.Library()

@register.filter(name='webp_conversion_filter')
def webp_conversion_filter(image_path):
    """
    Converts an image to WebP format and returns the WebP URL.
    """
    if not image_path:
        return image_path  # Return the original path if none is provided

    # Define the WebP file path
    base, ext = os.path.splitext(image_path)
    webp_path = f"{base}.webp"

    # Absolute path for conversion
    original_file = os.path.join(settings.MEDIA_ROOT, image_path)
    converted_file = os.path.join(settings.MEDIA_ROOT, webp_path)

    # Check if the WebP version already exists
    if os.path.exists(converted_file):
        return webp_path

    # Convert the image to WebP
    try:
        with Image.open(original_file) as img:
            img.save(converted_file, format="webp")
        return webp_path
    except Exception as e:
        # Log error and return the original image path if conversion fails
        print(f"Error converting image: {e}")
        return image_path
