import os
import platform

from datetime import datetime
from .constants import INPUT_DIR, OUTPUT_DIR

class Setup_Info:
    __slots__ = (
        'timestamp',
        'os',
        'extract_from'
    )

    def __init__(self):
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        self.os = ''
        self.extract_from = ''

def determine_os():
    os = platform.system()
    
    if os == "Darwin":
        return "Mac"
    return os

def run(args):
    info = Setup_Info()

    # Get OS
    info.os = determine_os()
    
    # Set extract path if given
    if args.path:
        info.extract_from = os.path.abspath(args.path)

    # If no input folders exist make them
    if not os.path.isdir(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    return info
