__author__ = "MrOctopus / Neverlost"

import pyWhatsUpp.arguments as arguments
import pyWhatsUpp.setup as setup
import pyWhatsUpp.extractor as extractor
import pyWhatsUpp.collector as collector

def main():
    args = arguments.get()
    info = setup.run(args)

    info.log.info("------------------------ pyWhatsUpp ------------------------")

    info.log.info(f"Automatic WhatsApp folder detection is set to: {info.auto}")
    info.log.info(f"The operating system is set to: {info.os}")
    info.log.info("Session logs are stored in log.txt")
    
    if args.path:
        info.log.info(f"A manual input has been set to: {info.path}")

    info.log.info("------------------------------------------------------------")

    info.log.info("- Extracting all WhatsApp artifacts -")
    if not extractor.run(info):
        info.log.error("- Failed to find any WhatsApp artifacts, aborting. Consider trying other arguments -")
        # We return here because the other steps are not possible if the extractor did not finish
        return

    info.log.info("- Processing relevant WhatsApp forensic artifacts -")
    if not collector.run(info):
        info.log.error(" - Failed to find and process any relevant forensic WhatsApp artifacts -")

    info.log.info("- Successfully extracted and processed all WhatsApp artifacts -")
    info.log.info(f"Extracted session data can be found at: {info.input}")
    info.log.info(f"Processed session data can be found at: {info.output}")

if __name__ == "__main__":
    main()