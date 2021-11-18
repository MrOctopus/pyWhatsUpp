import os
import glob
import shutil
import binascii
import re

_EVENT_RE = re.compile("6c6f6722(.*?)74696d657374616d70")
_USERNAME_RE = re.compile("2265787069726174696f6e22.*?22(.*?)22")

def _carve_file_for_events(file_path):
    events = []

    with open(file_path, 'rb') as file:
        hexdump = binascii.hexlify(file.read())

        for match in _EVENT_RE.finditer(hexdump.decode()):
            event = str(binascii.a2b_hex(match.group(1)))
            # Since we cannot decode the string directly, we need to pretty up the string with hacks
            # START: Find first space to remove gibberish
            # END: -4 removes trailing "\t'
            event = event[event.find(' ') + 1:-4]

            events.append(event)

    return events

def _carve_file_for_username(file_path):
    usernames = []

    with open(file_path, 'rb') as file:
        hexdump = binascii.hexlify(file.read())

        for match in _USERNAME_RE.finditer(hexdump.decode()):
            username = binascii.a2b_hex(match.group(1)).decode()
            usernames.append(f"Possible username,\"{username}\"")

    return usernames

def _collect_general_logs(info, logs):
    if len(logs) < 1:
        return False

    general_logs_dir = os.path.join(info.output, "Chromium", "General Logs")
    os.makedirs(general_logs_dir, exist_ok=True)

    for i, log in enumerate(logs):
        log_dest = os.path.join(general_logs_dir, f"{i}_{os.path.basename(log)}")
        shutil.copy2(log, log_dest)

    return True

def _collect_process_logs(info, logs):
    if len(logs) < 1:
        return False

    process_logs_dir = os.path.join(info.output, "Chromium", "Process Logs")
    os.makedirs(process_logs_dir, exist_ok=True)

    for i, log in enumerate(logs):
        log_dest = os.path.join(process_logs_dir, f"{i}_{os.path.basename(log)}")
        shutil.copy2(log, log_dest)
    
    return True

def _collect_event_logs(info, logs):
    if len(logs) < 1:
        return False

    event_logs_dir = os.path.join(info.output, "Chromium", "Event Logs")
    os.makedirs(event_logs_dir, exist_ok=True)
    num_logs = 0

    for log in logs:
        events = _carve_file_for_events(log)

        if len(events) < 1:
            continue

        log_dest = os.path.join(event_logs_dir, f"{num_logs}_{os.path.basename(log)}")

        with open(log_dest, 'w+') as file:
            file.write('\n'.join(events))
        
        shutil.copystat(log, log_dest)
        num_logs += 1

    if num_logs < 1:
        return False

    return True

def _collect_username_logs(info, logs):
    if len(logs) < 1:
        return False

    num_usernames = 0

    for log in logs:
        usernames = _carve_file_for_username(log)

        if len(usernames) < 1:
            continue

        info.extra_data.append('\n'.join(usernames))
        num_usernames += 1

    if num_usernames < 1:
        return False

    return True

def collect_logs(info):
    # Case insensitive search for Log files
    log_matches = glob.glob(
        os.path.join(info.input, '**', "*[Ll][Oo][Gg]*"), 
        recursive=True)
    general_logs = []
    process_logs = []
    event_logs = []

    for match in log_matches: 
        # We only care about file matches
        if not os.path.isfile(match):
            continue

        if "process" in match:
            process_logs.append(match)
        elif "leveldb" in match:
            event_logs.append(match)
        else:
            general_logs.append(match)

    ldb_matches = glob.glob(
        os.path.join(info.input, '**', "*.ldb"), 
        recursive=True)
    username_logs = []

    for match in ldb_matches:
        # We only care about file matches
        if os.path.isfile(match):
            username_logs.append(match)
    
    successful = 0

    successful += int(_collect_general_logs(info, general_logs))
    successful += int(_collect_process_logs(info, process_logs))
    successful += int(_collect_event_logs(info, event_logs))
    successful += int(_collect_username_logs(info, username_logs))

    return successful > 0
