import os
import shutil

from . import extract_windows
from . import extract_mac
from . import extract_linux

#from hashlib import sha256
def _copy_files(info, whatsapp_dirs):
    if (whatsapp_dirs is None) or (len(whatsapp_dirs) < 1):
        return False 

    # Create input dir
    os.mkdir(info.input)

    for path in whatsapp_dirs:
        sanitizied_path = path.replace(':', '_')
        sanitizied_path = sanitizied_path.replace(os.path.sep, '_')
        sanitizied_path = os.path.join(info.input, sanitizied_path)

        # Copy using shutil to preserve most metadata
        # shutil.copytree uses shutil.copy2 in the background 
        # (See https://docs.python.org/3/library/shutil.html)
        shutil.copytree(path, sanitizied_path)

    return True

def run(info):
    os = info.os

    # Manual
    if (not info.auto) and (info.path):
        whatsapp_dirs = [info.path]
    # Automatic
    elif os == "Windows":
        whatsapp_dirs = extract_windows.run(info)
    elif os == "Mac":
        whatsapp_dirs = extract_mac.run(info)
    elif os == "Linux":
        whatsapp_dirs = extract_linux.run(info)

    # Copy files
    if not _copy_files(info, whatsapp_dirs):
        return False

    # Generate file hashes if flag is enabled
    # TBD

    return True