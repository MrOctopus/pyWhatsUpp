from . import chromium
from . import firefox

def run(info):
    successful_collections = 0

    successful_collections += chromium.collect(info)
    successful_collections += firefox.collect(info)

    if successful_collections < 1:
        return False
    else:
        info.log.info(f"Collected a total of '{successful_collections}' WhatsApp artifact collections")
        return True