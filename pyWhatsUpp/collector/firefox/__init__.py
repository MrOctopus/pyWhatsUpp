__all__ = ('logs')
from .logs import collect_logs

def collect(info):
    return collect_logs(info)