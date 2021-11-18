__all__ = ('logs')
from .logs import collect_logs

def collect(info):
    successful_steps = 0

    successful_steps += int(collect_logs(info))

    return successful_steps > 0