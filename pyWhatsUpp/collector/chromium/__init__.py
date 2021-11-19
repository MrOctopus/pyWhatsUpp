__all__ = ('images', 'logs')
from .images import collect_images
from .logs import collect_logs

def collect(info):
    return collect_images(info) + collect_logs(info)