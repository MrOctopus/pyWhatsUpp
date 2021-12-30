from . import leveldb
from . import sqlite

def run(info):
    successful_extractions = 0

    successful_extractions += leveldb.extract(info)
    successful_extractions += sqlite.extract(info)

    if successful_extractions < 1:
        return False
    else:
        info.log.info(f"Extracted a total of '{successful_extractions}' WhatsApp artifact collections")
        return True