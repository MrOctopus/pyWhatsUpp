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

## Planned features

1. Better logging (Very soon)
2. Linux extraction

## Thanks to

* Ntninja for [mozidb](https://gitlab.com/ntninja/moz-idb-edit/-/tree/master)
* cclgroupltd for [ccl_chrome_indexeddb](https://github.com/cclgroupltd/ccl_chrome_indexeddb)

## Resources for further reading

* Firefox IndexDB proprietary format formatting: https://stackoverflow.com/questions/54920939/parsing-fb-puritys-firefox-idb-indexed-database-api-object-data-blob-from-lin

* Interpreting WhatsApp event logs: https://www.semanticscholar.org/paper/Browser-Forensic-Investigations-of-WhatsApp-Web-Paligu-Varol/0054508526255eff5c15de5ab3194591e842d731
* General WhatsApp forensics how-to: https://blog.group-ib.com/whatsapp_forensic_artifacts