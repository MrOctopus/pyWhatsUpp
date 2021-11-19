# pyWhatsUpp

A forensic tool to automatically extract as many artifacts as possible from the WhatsApp desktop/web client

## Features

### Extraction

* Automatic
    - From an automatically determined WhatsApp drive and OS (Useful for extraction on the same device)
    - From a user defined root directory/drive and OS (Useful for mounted drives)
* Manual
    - From a user defined WhatsApp data directory (Useful for unusual(?) WhatsApp locations)

### Collection

* Cached contact avatars
* General logs
* Processing logs
* Event logs
* WhatsApp username

### Interpretation

* pyWhatsUpp will try to enrich event logs with explanations and interpretations

### Hashing

* pyWhatsUpp supports outputting a list of all extracted file hashes

## Support

Although pyWhatsUpp can be run on every platform that supports python,
extraction can only be performed on data/mounts deriven from supported OSes.

### OS

* Windows (Win7-Win11)
* MacOS

Not supported:

* Linux

### Client

* WhatsApp desktop for Windows
* WhatsApp desktop for Mac
* Firefox browser
* Microsoft edge browser
* Chrome browser
* Opera browser

Not supported:

* Safari Browser

## Usage

```
Run pyWhatsUpp in-place with automatic extraction:
python run.py

Show verbose logs and generate sha256 hashes:
python run.py -v -ha

Run pyWhatsUpp on a specific WhatsApp folder
python run.py -i folderpath

Run pyWhatsUpp on a mounted windows installation drive and perform automatic extraction:
python run.py -a -os Windows -i mountedrootpath
```
### Notes

Whilst pyWhatsUpp attempts to preserve the file metadata of extracted artifacts the best it can, a separate forensics image should also be made to ensure that the original file metadata can be compared against. Noteably, the python library that pyWhatsUpp uses to copy metadata (shutil) is not reliable enough to ensure the integrity of Accessed and Created timestamps.

## Thanks to

* Ntninja for [mozidb](https://gitlab.com/ntninja/moz-idb-edit/-/tree/master)
* cclgroupltd for [ccl_chrome_indexeddb](https://github.com/cclgroupltd/ccl_chrome_indexeddb)

## Resources for further reading

* Firefox IndexDB proprietary format formatting: https://stackoverflow.com/questions/54920939/parsing-fb-puritys-firefox-idb-indexed-database-api-object-data-blob-from-lin

* Interpreting WhatsApp event logs: https://www.semanticscholar.org/paper/Browser-Forensic-Investigations-of-WhatsApp-Web-Paligu-Varol/0054508526255eff5c15de5ab3194591e842d731
* General WhatsApp forensics know-how: https://blog.group-ib.com/whatsapp_forensic_artifacts