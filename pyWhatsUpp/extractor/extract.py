from . import extract_windows
from . import extract_mac
from . import extract_linux

#from hashlib import sha256

def run(info):
    os = info.os

    if os == "Windows":
        return extract_windows.run(info)
    elif os == "Mac":
        return extract_mac.run(info)
    elif os == "Linux":
        return extract_linux.run(info)

    # Error!!
    return False