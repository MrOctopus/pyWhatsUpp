import os
import glob
import shutil

from pyWhatsUpp.utils.ccl_chrome_indexddb import ccl_chromium_indexeddb
from pyWhatsUpp.utils.interpreter import get_event_type

_log_counter = 0

def _collect_event_logs(info, original_file, db_data):
    global _log_counter
    events = []

    for row in db_data["logs"].iterate_records():
        _dict = row.value
        events.append(_dict["log"][5:])

    if len(events) < 1:
        return False

    event_logs_dir = os.path.join(info.output, "Chromium", "Event Logs")
    os.makedirs(event_logs_dir, exist_ok=True)
    log_file = os.path.join(event_logs_dir, f"{_log_counter}.txt")

    with open(log_file, 'w+') as file:
        for event in events:
            file.write(f"{event} | {get_event_type(event)}\n")
    
    shutil.copystat(original_file, log_file)
    _log_counter += 1

    return True

def _collect_general_data(info, db_data):    
    data = []
    
    for row in db_data["user"].iterate_records():
        data.append((
            row.key.raw_key,
            row.value
        ))
    for row in db_data["wam"].iterate_records():
        data.append((
            row.key.raw_key,
            row.value
        ))

    if len(data) < 1:
        return False

    info.extra_data.append("Chromium data,below\n")
    for key, value in data:
        info.extra_data.append(f"\"{key}\",\"{value}\"")
    info.extra_data.append("\n")
    
    return True

def _collect_process_logs(info, original_file):
    global _log_counter

    process_logs_dir = os.path.join(info.output, "Chromium", "Process Logs")
    os.makedirs(process_logs_dir, exist_ok=True)
    log_file = os.path.join(process_logs_dir, f"{_log_counter}_{os.path.basename(original_file)}")

    try:
        shutil.copy2(original_file, log_file)
        _log_counter += 1
    except Exception:
        return False

    return True

def _collect_general_logs(info, original_file):
    global _log_counter

    general_logs_dir = os.path.join(info.output, "Chromium", "General Logs")
    os.makedirs(general_logs_dir, exist_ok=True)
    log_file = os.path.join(general_logs_dir, f"{_log_counter}_{os.path.basename(original_file)}")

    try:
        shutil.copy2(original_file, log_file)
        _log_counter += 1
    except Exception:
        return False

    return True

def collect_logs(info):
    # Case insensitive search for Log files
    log_matches = glob.glob(
        os.path.join(info.input, '**', "*[Ll][Oo][Gg]*"), 
        recursive=True)
    processed_dbs = []
    successful = 0

    for match in log_matches:
        if not os.path.isfile(match):
            continue

        if "leveldb" in match:
            match_dir = os.path.dirname(match)

            if match_dir in processed_dbs:
                continue
            
            processed_dbs.append(match_dir)


            try:
                db = ccl_chromium_indexeddb.WrappedIndexDB(match_dir)
                db_data = db["wawc"]
            except Exception as e:
                continue

            successful += int(_collect_event_logs(info, match, db_data))
            successful += int(_collect_general_data(info, db_data))

        elif "process" in match:
            successful += int(_collect_process_logs(info, match))
        else:
            successful += int(_collect_general_logs(info, match))

    return successful