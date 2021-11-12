import os
import argparse

import pyWhatsUpp.arguments as arguments
import pyWhatsUpp.setup as setup
import pyWhatsUpp.extractor as extractor
import pyWhatsUpp.collector as collector

def main():
    args = arguments.get()
    info = setup.run(args)

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