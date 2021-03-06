import os
import glob
import shutil

from pyWhatsUpp.utils.mozidb import mozidb
from pyWhatsUpp.utils.interpreter import get_event_type

_log_counter = 0

def _extract_event_logs(info, original_file, db_data):
    global _log_counter
    events = []

    for key in db_data:
        _dict = db_data[key]

        if "log" in _dict:
            events.append((
                key,
                _dict["log"][5:]
            ))

    if len(events) < 1:
        return False

    event_logs_dir = os.path.join(info.output, "SQLite", "Event Logs")
    os.makedirs(event_logs_dir, exist_ok=True)
    log_file = os.path.join(event_logs_dir, f"{_log_counter}.txt")

    info.log.info(f"Interpeting data in {log_file}")

    with open(log_file, 'w+') as file:
        for key, event in events:
            event_type = get_event_type(event)
            db_data.pop(key)

            if info.strict and event_type == '?':
                continue

            file.write(f"{event} | {event_type}\n")
    
    shutil.copystat(original_file, log_file)
    _log_counter += 1

    return True

def _extract_general_data(info, db_data):    
    data = []
    
    for _dict in db_data.values():
        if "key" in _dict and "value" in _dict:
            data.append((
                _dict["key"],
                _dict["value"]
            ))

    if len(data) < 1:
        return False

    info.extra_data.append("SQLite data,below")
    for key, value in data:
        info.extra_data.append(f"\"{key}\",\"{value}\"")
    info.extra_data.append("\n")

    db_data.clear()
    
    return True

def extract_logs(info):
    # search for sqlite or Ldb files
    sqlite_matches = glob.glob(
        os.path.join(info.input, '**', "*wcaw.sqlite"), 
        recursive=True)
    successful = 0

    for match in sqlite_matches: 
        # We only care about file matches
        if not os.path.isfile(match):
            continue

        try:
            db = mozidb.IndexedDB(match)
            db_data = db.read_objects()
        except Exception:
            continue

        successful += int(_extract_event_logs(info, match, db_data))
        successful += int(_extract_general_data(info, db_data))

    return successful
