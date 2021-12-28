import os
import platform
import logging
import logging.config

from datetime import datetime

class SetupInfo:
    __slots__ = (
        'timestamp',
        'extra_data',
        'log',
        'os',
        'input',
        'output',
        'path',
        'auto',
        'hash',
        'strict'
    )

    def __init__(self):
        # Internal
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.extra_data = []
        self.log = None

        # User defined
        self.os = ''
        self.input = ''
        self.output = ''
        self.path = ''
        self.auto = True
        self.hash = False
        self.strict = False

    def dump_to_output(self):
        if not os.path.exists(self.output):
            return

        extra_data_dest = os.path.join(self.output, "general.csv")

        with open(extra_data_dest, 'w+') as file:
            file.write(f"pyWhatsUpp Timestamp,{self.timestamp}\n\n")

            if self.extra_data:
                file.write('\n'.join(self.extra_data))



def _determine_os():
    os = platform.system()
    
    # Easier to understand Mac than Darwin
    if os == "Darwin":
        return "Mac"

    return os

def _init_logger(args):
    log_format = "%(asctime)s [%(levelname).4s] %(message)s"

    logging.basicConfig(
        filename=os.path.join(os.path.dirname(__file__), '..', "log.txt"),
        filemode='a',
        level=logging.NOTSET, 
        format=log_format
    )

    log = logging.getLogger("pyWhatsUpp")

    if args.verbose:
        formatter = logging.Formatter(log_format)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)

        log.addHandler(console)

    return log


def run(args):
    info = SetupInfo()
    info.log = _init_logger(args)

    # We get the top_dir using the __file__ variable to ensure
    # the CWD does not affect pathing
    top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_dir = os.path.join(top_dir, 'collected')
    output_dir = os.path.join(top_dir, 'processed')

    # If no input folders exist make them
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Set info specific input:
    info.input = os.path.join(input_dir, info.timestamp)
    info.output = os.path.join(output_dir, info.timestamp)

    info.auto = args.auto
    info.hash = args.hash
    info.strict = args.strict

    # Set extract path if given
    if args.path:
        info.path = os.path.abspath(args.path)

    # Determine OS if no arg has been given
    if args.os:
        info.os = args.os
    else:
        info.os = _determine_os()

    return info