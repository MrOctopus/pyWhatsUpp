import os
import platform

from datetime import datetime

def _determine_os():
    os = platform.system()
    
    # Easier to understand Mac than Darwin
    if os == "Darwin":
        return "Mac"

    return os

def run(args):
    info = Setup_Info()

    # We get the top_dir using the __file__ variable to ensure
    # the CWD does not affect pathing
    top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_dir = os.path.join(top_dir, 'original')
    output_dir = os.path.join(top_dir, 'processed')

    # If no input folders exist make them
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Set info specific input:
    info.input = os.path.join(input_dir, info.timestamp)
    info.output = os.path.join(output_dir, info.timestamp)

    # Determine OS if no arg has been given
    if args.os:
        info.os = args.os
    else:
        info.os = _determine_os()

    # Set extraction to automatic if flag is set
    info.auto = args.auto

    # Set extract path if given
    if args.path:
        info.path = os.path.abspath(args.path)

    return info

class Setup_Info:
    __slots__ = (
        'timestamp',
        'os',
        'input',
        'output',
        'path',
        'auto'
    )

    def __init__(self):
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        self.os = ''
        self.input = ''
        self.output = ''
        self.path = ''
        self.auto = True