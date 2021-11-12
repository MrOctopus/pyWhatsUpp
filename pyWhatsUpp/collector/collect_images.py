import os
import binascii
import re

_JPEG_RE = re.compile("ffd8ff(.*?)ffd9")

def _carve_file_for_jpeg(file_path, found_images):
    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'rb') as file:
        hexdump = binascii.hexlify(file.read())

        for match in _JPEG_RE.finditer(hexdump.decode()):
            image_binary = binascii.a2b_hex(match[0])
            found_images.append(image_binary)

def run(info):
    found_images = []

    for _dir in os.listdir(info.input):
        # See https://blog.group-ib.com/whatsapp_forensic_artifacts
        avatar_cache = os.path.join(info.input, _dir, "Cache", "data_2")
        _carve_file_for_jpeg(avatar_cache, found_images)

    # Could not find any images
    if len(found_images) < 1:
        return False

    # We don't care if this fails
    try:
        os.mkdir(info.output)
    except FileExistsError:
        pass

    images_dir = os.path.join(info.output, "Avatars")
    os.mkdir(images_dir)

    for i, image in enumerate(found_images):
        image_path = os.path.join(images_dir, f"{i}.jpg")

        with open(image_path,'wb') as file:
            file.write(image)

    return True