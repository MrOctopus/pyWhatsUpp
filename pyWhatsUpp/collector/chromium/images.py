import os
import glob
import shutil
import binascii
import re

_JPEG_RE = re.compile("ffd8ff(.*?)ffd9")

def _carve_file_for_jpeg(file_path):
    images = []

    with open(file_path, 'rb') as file:
        hexdump = binascii.hexlify(file.read())

        for match in _JPEG_RE.finditer(hexdump.decode()):
            image_binary = binascii.a2b_hex(match[0])
            images.append(image_binary)

    return images

def _collect_avatar_images(info, avatar_caches):
    if len(avatar_caches) < 1:
        return False

    images_dir = os.path.join(info.output, "Chromium", "Contact Avatars")
    os.makedirs(images_dir, exist_ok=True)
    num_images = 0

    for avatar_cache in avatar_caches:
        images = _carve_file_for_jpeg(avatar_cache)
        
        for image in images:
            image_dest = os.path.join(images_dir, f"{num_images}.jpg")

            with open(image_dest,'wb') as file:
                file.write(image)

            shutil.copystat(avatar_cache, image_dest)
            num_images += 1

    if num_images < 1:
        return False

    info.log.info(f"Created new contact avatars folder containing a total of '{num_images}' images")
    return True

def collect_images(info):
    cache_matches = glob.glob(
        os.path.join(info.input, '**', "*data_2"), 
        recursive=True)
    avatar_caches = []

    for match in cache_matches: 
        # We only care about file matches
        if os.path.isfile(match):
            avatar_caches.append(match)

    return _collect_avatar_images(info, avatar_caches)