__all__ = ('images', 'logs')
from .images import collect_images
from .logs import collect_logs

def collect(info):
    successful_steps = 0

    successful_steps += int(collect_images(info))
    successful_steps += int(collect_logs(info))

    return successful_steps > 0