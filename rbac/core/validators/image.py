from django.core.exceptions import ValidationError
import os
from rbac.core.constants import ALLOWED_IMAGE_EXTENSIONS, MAX_IMAGE_SIZE_MB

def validate_image_size(image):
    if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image size must be less than {MAX_IMAGE_SIZE_MB}MB.")

def validate_image_extension(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(f"Image extension {ext} is not allowed.")