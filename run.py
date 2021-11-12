import os
import argparse

import pyWhatsUpp.setup as setup
import pyWhatsUpp.extractor as extractor
import pyWhatsUpp.collector as collector

def get_arguments():
    def is_dir(string):
        if not os.path.isdir(string):
            raise argparse.ArgumentTypeError("The input path must be a directory")

        return string

    arg_parser = argparse.ArgumentParser(prog= "pyWhatsUpp")
    arg_parser.add_argument("-v", dest= "verbose", help="Verbose", type=bool)
    arg_parser.add_argument("-i", dest= "path", help="Path to manual folder", type=is_dir)

    return arg_parser.parse_args()

def main():
    arguments = get_arguments()
    info = setup.run(arguments)

    if not extractor.run(info):
        return

    if not collector.run(info):
        return

    # SUCCESS


    #if not info.

    #run_extractor()
    #run_

    #find


if __name__ == "__main__":
    main()