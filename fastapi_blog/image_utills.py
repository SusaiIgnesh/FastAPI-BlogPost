import uuid ## Used for creating the unique id from image upload
from io import BytesIO # Working with image bytes in memory
from pathlib import Path # File opaertions


from PIL import Image, ImageOps # Image functionality

#Image upload the path
PROFILE_PICS_DIR = Path("media/profile_pics")

# Image file reading and processing and storing image in the directory
def process_profile_image(content: bytes) -> str:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(img, (300,300), method = Image.Resampling.LANCZOS)

        if img.mode in ("RGBA","LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = PROFILE_PICS_DIR / filename

        PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

        img.save(filepath, "JPEG", quality=85, optimize=True)

    return filename
    

## Deleting the file 
def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return None
    
    filepath = PROFILE_PICS_DIR / filename

    if filepath.exists():
        filepath.unlink()
