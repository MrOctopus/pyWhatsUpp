from . import chromium
from . import firefox

def run(info):
    successful_extractions = 0

    successful_extractions += chromium.extract(info)
    successful_extractions += firefox.extract(info)

    if successful_extractions < 1:
        return False
    else:
        info.log.info(f"Extracted a total of '{successful_extractions}' WhatsApp artifact collections")
        return True