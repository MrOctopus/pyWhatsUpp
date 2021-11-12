from . import collect_images
from . import collect_logs

def run(info):
    successful_steps = 0

    successful_steps += int(collect_images.run(info))
    successful_steps += int(collect_logs.run(info))

    return successful_steps > 0