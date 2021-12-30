__all__ = ('images', 'logs')
from .images import extract_images
from .logs import extract_logs

def extract(info):
    return extract_images(info) + extract_logs(info)