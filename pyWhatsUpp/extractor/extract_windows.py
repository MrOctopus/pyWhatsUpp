import os
import ctypes
import getpass
import shutil

from ..constants import INPUT_DIR

def _get_windows_drive():
    kernel_dll = ctypes.windll.kernel32
    windows_dir = ctypes.create_unicode_buffer(1024)

    # Attempt to grab windows_directory using kernel32.dll
    # because os.environ['SYSTEMDRIVE'] can be overridden
    if kernel_dll.GetWindowsDirectoryW(windows_dir, 1024) == 0:
        return ''

    return f"{os.path.splitdrive(windows_dir.value)[0]}{os.path.sep}"

def _manual(info, drive):
    pass


def _automatic(info, drive):
    username = getpass.getuser()

    if not username:
        return False

     # See WhatsApp artifacts in Windows section
    # in https://blog.group-ib.com/whatsapp_forensic_artifacts
    possible_whatsapp_locations = (
        os.path.join(drive, "Program Files", "WhatsApp"),
        os.path.join(drive, "Program Files (x86)", "WhatsApp"),
        os.path.join(drive, "Users", username, "AppData", "Roaming", "WhatsApp"),
        os.path.join(drive, "Users", username, "AppData", "Local", "WhatsApp"),
        os.path.join(drive, "Users", username, "AppData", "Local", "VirtualStore", "Program Files", "WhatsApp"),
        os.path.join(drive, "Users", username, "AppData", "Local", "VirtualStore", "Program Files (x86)", "WhatsApp"),
    )
    actual_whatsapp_locations = []

    for possible_dir in possible_whatsapp_locations:
        if os.path.isdir(possible_dir):
            actual_whatsapp_locations.append(possible_dir)

    if len(actual_whatsapp_locations) < 1:
        return False

    input_dir_current = os.path.join(INPUT_DIR, info.timestamp)
    os.mkdir(input_dir_current)

    for actual_dir in actual_whatsapp_locations:
        sanitizied_path = actual_dir.replace(':', '_')
        sanitizied_path = sanitizied_path.replace(os.path.sep, '_')
        sanitizied_path = os.path.join(input_dir_current, sanitizied_path)

        # Copy using shutil to preserve most metadata
        # shutil.copytree uses shutil.copy2 in the background 
        # (See https://docs.python.org/3/library/shutil.html)
        shutil.copytree(actual_dir, sanitizied_path)

    # Copy using shutil to preserve metadata
    #sha256(test).hexdigest()


def run(info):
    main_drive = _get_windows_drive()

    if not main_drive:
        return False

    if info.extract_from:
        return _manual(info, main_drive)
    else:
        return _automatic(info, main_drive)