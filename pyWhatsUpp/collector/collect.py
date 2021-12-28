import os
import shutil

from . import collect_windows
from . import collect_mac
from . import collect_linux

#from hashlib import sha256
def _copy_files(info, whatsapp_dirs):
    if (whatsapp_dirs is None) or (len(whatsapp_dirs) < 1):
        return False 

    # Create input and output dirs
    os.mkdir(info.input)
    os.mkdir(info.output)

    for path in whatsapp_dirs:
        sanitizied_path = path.replace(':', '_')
        sanitizied_path = sanitizied_path.replace(os.path.sep, '_')
        sanitizied_path = os.path.join(info.input, sanitizied_path)

        # Copy using shutil to preserve most metadata
        # shutil.copytree uses shutil.copy2 in the background 
        # (See https://docs.python.org/3/library/shutil.html)

        try:
            shutil.copytree(path, sanitizied_path)
        except Exception as e:
            info.log.error(f"Encounted an error when extracting a folder: {e}")
            info.log.error("This might have occured because a WhatsApp session is currently running")


    info.log.info(f"Extracted a total of '{len(whatsapp_dirs)}' WhatsApp data folders")

    return True

def run(info):
    os = info.os

    # Manual
    if (not info.auto) and (info.path):
        print("manual")
        whatsapp_dirs = [info.path]
    # Automatic
    elif os == "Windows":
        whatsapp_dirs = collect_windows.run(info)
    elif os == "Mac":
        whatsapp_dirs = collect_mac.run(info)
    elif os == "Linux":
        whatsapp_dirs = collect_linux.run(info)

    return _copy_files(info, whatsapp_dirs)