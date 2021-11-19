import os
import glob
import shutil
import binascii
import re

_JPEG_RE = re.compile("ffd8ff(.*?)ffd9")

_image_counter = 0

def _carve_file_for_jpeg(file_path):
    images = []

    with open(file_path, 'rb') as file:
        hexdump = binascii.hexlify(file.read())

        for match in _JPEG_RE.finditer(hexdump.decode()):
            image_binary = binascii.a2b_hex(match[0])
            images.append(image_binary)

    return images

def _collect_avatar_images(info, original_file):
    global _image_counter
    images = _carve_file_for_jpeg(original_file)

    if len(images) < 1:
        return False

    images_dir = os.path.join(info.output, "Chromium", "Contact Avatars")
    os.makedirs(images_dir, exist_ok=True)
        
    for image in images:
        image_file = os.path.join(images_dir, f"{_image_counter}.jpg")

        with open(image_file,'wb') as file:
            file.write(image)

        shutil.copystat(original_file, image_file)
        _image_counter += 1

    return True

def collect_images(info):
    cache_matches = glob.glob(
        os.path.join(info.input, '**', "*data_2"), 
        recursive=True)
    successful = 0

    for match in cache_matches: 
        if os.path.isfile(match):
            successful += int(_collect_avatar_images(info, match))

    return successful