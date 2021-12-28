import os

def _get_root_drive(info):
    # User has manually set root for detecting
    if info.path:
        return info.path

    return os.path.sep

def _get_users(root):
     users_dir = os.path.join(root, "Users")

    # Ignore:
    # Standard user directories
    
     users = [
          name for name in os.listdir(users_dir) 
          if os.path.isdir(os.path.join(users_dir, name))
     ]
     
     return users

def _get_user_whatsapp_locations(root, username):
    user_dir = os.path.join(root, "Users", username)

    # Note:
    # I have yet to find where Safari stores its data
    user_whatsapp_locations = (
            os.path.join(user_dir, "Library", "Logs", "WhatsApp"),
            os.path.join(user_dir, "Library", "Saved Application State", "WhatsApp.savedState"),
            os.path.join(user_dir, "Library", "Containers", "com.rockysandstudio.app-for-whatsappp"),
            os.path.join(user_dir, "Library", "Containers", "desktop.WhatsApp"),
            os.path.join(user_dir, "Library", "Caches", "WhatsApp.ShipIt"),
            os.path.join(user_dir, "Library", "Caches", "WhatsApp"),
            os.path.join(user_dir, "Library", "Application Support", "WhatsApp.ShipIt"),
            os.path.join(user_dir, "Library", "Application Support", "WhatsApp"),
            os.path.join(user_dir, "Library", "Application Support", "Google", "Chrome", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
            os.path.join(user_dir, "Library", "Application Support", "Microsoft", "Edge", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
            os.path.join(user_dir, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "Default", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
            os.path.join(user_dir, "Library", "Application Support", "Opera Software", "Opera Stable", "IndexedDB", "https_web.whatsapp.com_0.indexeddb.leveldb"),
        )

    return user_whatsapp_locations

def _get_user_whatsapp_locations_advanced(root, username):
    document_dir = os.path.join(root, "Users", username, "Library", "Mobile Documents")
    document_whatsapp_locations = []

    if os.path.exists(document_dir):
        for document in os.listdir(document_dir):            
            if not "WhatsApp" in document:
                continue

            account_dir = os.path.join(document_dir, document)

            if not os.path.isdir(account_dir):
                continue

            whatsapp_location = os.path.join(account_dir, "Accounts")
            document_whatsapp_locations.append(whatsapp_location)

    return document_whatsapp_locations

def _get_user_firefox_whatsapp_locations(root, username):
    firefox_profile_dir = os.path.join(root, "Users", username, "Library", "Application Support", "Firefox", "Profiles")
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

    # See WhatsApp artifacts in Mac section
    # in https://blog.group-ib.com/whatsapp_forensic_artifacts
    possible_whatsapp_locations = [
        os.path.join(root, "Applications", "WhatsApp.app"),
        os.path.join(root, "Applications", "._WhatsApp.app"),
    ]

    for username in usernames:
        possible_whatsapp_locations.extend(_get_user_whatsapp_locations(root, username))
        possible_whatsapp_locations.extend(_get_user_firefox_whatsapp_locations(root, username))
        possible_whatsapp_locations.extend(_get_user_whatsapp_locations_advanced(root, username))

    found_whatsapp_locations = [
        _dir for _dir in possible_whatsapp_locations
        if os.path.isdir(_dir)
    ]

    return found_whatsapp_locations