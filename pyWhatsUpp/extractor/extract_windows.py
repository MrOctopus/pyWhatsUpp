import os
import ctypes
import getpass

def _get_root_drive(info):
    # User has manually set root for detecting
    if info.path:
        return info.path
    
    kernel_dll = ctypes.windll.kernel32
    windows_dir = ctypes.create_unicode_buffer(1024)

    # Attempt to grab windows_directory using kernel32.dll
    # because os.environ['SYSTEMDRIVE'] can be overridden
    if kernel_dll.GetWindowsDirectoryW(windows_dir, 1024) == 0:
        return ''

    return f"{os.path.splitdrive(windows_dir.value)[0]}{os.path.sep}"

def run(info):
    main_drive = _get_root_drive(info)

    if not main_drive:
        return False

    username = getpass.getuser()

    if not username:
        return False

     # See WhatsApp artifacts in Windows section
    # in https://blog.group-ib.com/whatsapp_forensic_artifacts
    possible_whatsapp_locations = (
        os.path.join(main_drive, "Program Files", "WhatsApp"),
        os.path.join(main_drive, "Program Files (x86)", "WhatsApp"),
        os.path.join(main_drive, "Users", username, "AppData", "Roaming", "WhatsApp"),
        os.path.join(main_drive, "Users", username, "AppData", "Local", "WhatsApp"),
        os.path.join(main_drive, "Users", username, "AppData", "Local", "VirtualStore", "Program Files", "WhatsApp"),
        os.path.join(main_drive, "Users", username, "AppData", "Local", "VirtualStore", "Program Files (x86)", "WhatsApp"),
        os.path.join(main_drive, "Users", username, "Appdata", "Local", "Google", "Chrome", "User Data", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb")
    )
    found_whatsapp_locations = []

    for possible_dir in possible_whatsapp_locations:
        if os.path.isdir(possible_dir):
            found_whatsapp_locations.append(possible_dir)

    return found_whatsapp_locations

    #sha256(test).hexdigest()