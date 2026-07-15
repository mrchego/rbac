import os
import uuid


def generic_upload_path(instance, filename, subfolder):
    """
    Generate a unique upload path.

    Example:
    avatars/3f5d8c0d-6a3f-4c0d-a2c6-8f1f4c0d2b9a.jpg
    """
    _, ext = os.path.splitext(filename)
    filename = f"{uuid.uuid4()}{ext.lower()}"

    return os.path.join(subfolder, filename)


def avatar_upload_path(instance, filename):
    return generic_upload_path(
        instance,
        filename,
        "avatars",
    )


def company_logo_light_upload_path(instance, filename):
    return generic_upload_path(
        instance,
        filename,
        "company/logos/light",
    )


def company_logo_dark_upload_path(instance, filename):
    return generic_upload_path(
        instance,
        filename,
        "company/logos/dark",
    )