__all__ = ('logs')
from .logs import extract_logs

def extract(info):
    return extract_logs(info)