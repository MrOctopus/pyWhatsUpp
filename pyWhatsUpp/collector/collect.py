from . import chromium
from . import firefox

def run(info):
    successful_steps = 0

    successful_steps += int(chromium.collect(info))
    successful_steps += int(firefox.collect(info))

    return successful_steps > 0