import boto3
from PIL import Image
from typing import Tuple
from espy_pdfier.util import CONSTANTS
import os

def is_greater_than_allowed_size(image_path):
    return os.path.getsize(image_path) > CONSTANTS.IMAGE_SIZE_MB * 1024 * 1024

def resize_image(image_path, size):
    with Image.open(image_path) as image:
        image.thumbnail(size)
        return image

def store_image_in_s3(image, bucket_name, key):
    s3 = boto3.client('s3', aws_access_key_id=CONSTANTS.ACCESS_KEY, aws_secret_access_key=CONSTANTS.SECRET_KEY)
    with image as img:
        img.save(key)
        s3.upload_file(key, bucket_name, key)

def resize_and_store_images(image_path: str, 
                            bucket_name: str, 
                            app: str, 
                            thumbnail_size: Tuple[int, int] = (100, 100), 
                            big_image_size: Tuple[int, int] = (800, 800), 
                            raw_image_size: Tuple[int, int] = (1920, 1080)):
    if is_greater_than_allowed_size(image_path):
        raise ValueError("Image size exceeds the allowed limit.")

    _, extension = os.path.splitext(image_path)

    thumbnail_key = f"{app}_thumbnail{extension}"
    big_image_key = f"{app}_big_image{extension}"
    raw_image_key = f"{app}_raw_image{extension}"

    thumbnail_image = resize_image(image_path, thumbnail_size)
    big_image = resize_image(image_path, big_image_size)
    raw_image = resize_image(image_path, raw_image_size)

    store_image_in_s3(thumbnail_image, bucket_name, thumbnail_key)
    store_image_in_s3(big_image, bucket_name, big_image_key)
    store_image_in_s3(raw_image, bucket_name, raw_image_key)
