import os
import argparse

def _is_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("The input path must be a directory")

    return string

def _is_valid_os(string):
    lowercase = string.lower()

    if not lowercase in ('windows', 'mac', 'linux'):
        raise argparse.ArgumentTypeError("The OS must be of a supported type [Windows, Mac, Linux]")

    return lowercase.capitalize()

def get():
    arg_parser = argparse.ArgumentParser(prog= "pyWhatsUpp")
    arg_parser.add_argument("-v", "--verbose", dest="verbose", help="Verbose mode", action="store_true", default=False)
    arg_parser.add_argument("-ha", "--hash", dest="hash", help="Generate hashes", action="store_true", default=False)
    arg_parser.add_argument("-a", "--automatic", dest="auto", help="Automatic detection", action="store_true", default=None)
    arg_parser.add_argument("-si", "--strict-interpret", dest="strict", help="Strict interpretation", action="store_true", default=False)
    arg_parser.add_argument("-os", "--system", dest="os", help="OS type", type=_is_valid_os, default=None)
    arg_parser.add_argument("-i", "--input", dest="path", help="Directory path", type=_is_dir)

    # We parse the args here to do some additional
    # obscure checks
    parsed_args = arg_parser.parse_args()

    # Determine if we are handling a root or single manual path
    if parsed_args.path and parsed_args.auto is None:
        parsed_args.auto = False
    else:
        parsed_args.auto = True

    # Require OS flag to be set if we are dealing with automatic detection and a root path
    if parsed_args.os is None and parsed_args.path and parsed_args.auto:
        arg_parser.error("If automatic folder detection is enabled and you have defined a root path, you MUST supply a -os argument")

    return parsed_args