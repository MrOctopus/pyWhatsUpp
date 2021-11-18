import os
import glob
import shutil

from pyWhatsUpp.utils.mozidb import mozidb

def _carve_indexdb_for_events(file_path):
    events = []

    try:
        db = mozidb.IndexedDB(file_path)

        for row in db.read_objects().values():
            try:
                event = row['log'][5:]
                events.append(event)
            except KeyError:
                pass
    except Exception:
        pass

    return events

def _carve_indexdb_for_username(file_path):
    usernames = []

    db = mozidb.IndexedDB(file_path)
    return usernames

def _collect_event_logs(info, databases):
    if len(databases) < 1:
        return False

    event_logs_dir = os.path.join(info.output, "Firefox", "Event Logs")
    os.makedirs(event_logs_dir, exist_ok=True)
    num_logs = 0

    for db in databases:
        events = _carve_indexdb_for_events(db)

        if len(events) < 1:
            continue

        log_dest = os.path.join(event_logs_dir, f"{num_logs}_{os.path.basename(db)}")

        with open(log_dest, 'w+') as file:
            file.write('\n'.join(events))
        
        shutil.copystat(db, log_dest)
        num_logs += 1

    if num_logs < 1:
        return False

    return True

def _collect_username_logs(info, databases):
    if len(databases) < 1:
        return False

    num_usernames = 0

    for db in databases:
        usernames = _carve_indexdb_for_username(db)

        if len(usernames) < 1:
            continue

        info.extra_data.append('\n'.join(usernames))
        num_usernames += 1

    if num_usernames < 1:
        return False

    return True

def collect_logs(info):
    # search for sqlite or Ldb files
    sqlite_matches = glob.glob(
        os.path.join(info.input, '**', "*wcaw.sqlite"), 
        recursive=True)
    sqlite_databases = []

    for match in sqlite_matches: 
        # We only care about file matches
        if not os.path.isfile(match):
            continue

        sqlite_databases.append(match)
    
    successful = 0

    successful += int(_collect_event_logs(info, sqlite_databases))
    #successful += int(_collect_username_logs(info, sqlite_databases))

    return successful > 0
