import cloudinary
import cloudinary.uploader

async def upload_image_to_cloudinary(image) -> str:
    img = Image.open(BytesIO(await image.read()))
    
    with BytesIO() as buffer:
        if image.content_type == "image/png":
            img.save(buffer, "webp", lossless=True)
        elif image.content_type == "image/jpeg":
            img.save(buffer, "webp", quality=85)
        elif image.content_type == "image/webp":
            img.save(buffer, "webp")
        buffer.seek(0)  # Rewind the buffer to the beginning for reading
        response = cloudinary.uploader.upload(buffer)
        return response["secure_url"]