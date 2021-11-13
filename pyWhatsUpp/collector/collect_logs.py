import os
import glob
import shutil
import binascii
import re

_EVENT_RE = re.compile("6c6f6722(.*?)74696d657374616d70")

def _collect_general_logs(info, logs):
    if len(logs) < 1:
        return False

    general_logs_dir = os.path.join(info.output, "General Logs")
    os.mkdir(general_logs_dir)

    for i, log in enumerate(logs):
        log_dest = os.path.join(general_logs_dir, f"{i}_{os.path.basename(log)}")
        shutil.copy2(log, log_dest)

    return True

def _collect_process_logs(info, logs):
    if len(logs) < 1:
        return False

    process_logs_dir = os.path.join(info.output, "Process Logs")
    os.mkdir(process_logs_dir)

    for i, log in enumerate(logs):
        log_dest = os.path.join(process_logs_dir, f"{i}_{os.path.basename(log)}")
        shutil.copy2(log, log_dest)
    
    return True

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

def _collect_event_logs(info, logs):
    if len(logs) < 1:
        return False

    event_logs_dir = os.path.join(info.output, "Event Logs")
    os.mkdir(event_logs_dir)
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

def run(info):
    input_glob = os.path.join(info.input, '**', '*[Ll][Oo][Gg]*')
    glob_matches = glob.glob(input_glob, recursive=True)

    # Could not find any log files
    if not glob_matches:
        return False

    general_logs = []
    process_logs = []
    event_logs = []

    for log in glob_matches: 
        if "process" in log:
            process_logs.append(log)
        elif "index" in log:
            event_logs.append(log)
        else:
            general_logs.append(log)

    successful = 0
    
    successful += int(_collect_general_logs(info, general_logs))
    successful += int(_collect_process_logs(info, process_logs))
    successful += int(_collect_event_logs(info, event_logs))

    return successful > 0