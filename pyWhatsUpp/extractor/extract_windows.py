import os
import ctypes

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

def _get_users(root):
    users_dir = os.path.join(root, "Users")

    # Ignore:
    # Standard user directories
    # Non directories

    users = [
        name for name in os.listdir(users_dir) 
        if os.path.isdir(os.path.join(users_dir, name)) and name not in ("Default", "Default User", "All Users", "Public")
    ]

    return users

def _get_user_whatsapp_locations(root, username):
    user_dir = os.path.join(root, "Users", username)
    user_whatsapp_locations = (
            os.path.join(user_dir, "AppData", "Roaming", "WhatsApp"),
            os.path.join(user_dir, "AppData", "Local", "WhatsApp"),
            os.path.join(user_dir, "AppData", "Local", "VirtualStore", "Program Files", "WhatsApp"),
            os.path.join(user_dir, "AppData", "Local", "VirtualStore", "Program Files (x86)", "WhatsApp"),
            os.path.join(user_dir, "Appdata", "Local", "Google", "Chrome", "User Data", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
            os.path.join(user_dir, "Appdata", "Local", "Microsoft", "Edge", "User Data", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
            os.path.join(user_dir, "Appdata", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb")
        )

    return user_whatsapp_locations

def _get_user_firefox_whatsapp_locations(root, username):
    firefox_profile_dir = os.path.join(root, "Users", username, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    firefox_whatsapp_locations = []

    if os.path.exists(firefox_profile_dir):
        for profile in os.listdir(firefox_profile_dir):
            profile_dir = os.path.join(firefox_profile_dir, profile)
            
            if not os.path.isdir(profile_dir):
                continue

            whatsapp_location = os.path.join(profile_dir, "storage", "default", "https+++web.whatsapp.com")
            firefox_whatsapp_locations.append(whatsapp_location)

    return firefox_whatsapp_locations

def run(info):
    root = _get_root_drive(info)

    if not root:
        return None

    usernames = _get_users(root)

    if not usernames:
        return None

     # See WhatsApp artifacts in Windows section
    # in https://blog.group-ib.com/whatsapp_forensic_artifacts
    possible_whatsapp_locations = [
        os.path.join(root, "Program Files", "WhatsApp"),
        os.path.join(root, "Program Files (x86)", "WhatsApp"),
    ]

    for username in usernames:
        possible_whatsapp_locations.extend(_get_user_whatsapp_locations(root, username))
        possible_whatsapp_locations.extend(_get_user_firefox_whatsapp_locations(root, username))

    found_whatsapp_locations = []

    for _dir in possible_whatsapp_locations:
        if os.path.isdir(_dir):
            found_whatsapp_locations.append(_dir)

    return found_whatsapp_locations