# See https://www.semanticscholar.org/paper/Browser-Forensic-Investigations-of-WhatsApp-Web-Paligu-Varol/0054508526255eff5c15de5ab3194591e842d731
# See https://hammer.purdue.edu/articles/thesis/WhatsApp_Forensics_Locating_Artifacts_in_Web_and_Desktop_Clients/8029109/files/14954516.pdf

# NOTE: This is a very inefficient way of doing interpretation.
# There are way better ways of doing this, but it works for now.
def get_event_type(string):
    string = string.lower()

    if "action," in string:
        if ",presence" in string:
            if ",available" in string:
                return "User is available"
            elif ",unavailable" in string:
                return "User is unavailable"
        if ",chatstate" in string:
            if ",composing" in string:
                return "User is typing a message"
            elif ",paused" in string:
                return "User has stopped typing a message"
        elif "message" in string:
            if ",image" in string:
                return "User has sent an image"
            elif ",video" in string:
                return "User has sent a video"
            elif ",chat" in string:
                return "User has sent a message"
            elif ",vcard" in string:
                return "User has sent contact information"
            elif ",document" in string:
                return "User has sent a document"
            elif ",ptt" in string:
                return "User has sent an audio message"
        elif ",msg,relay" in string:
            if ",chat" in string:
                return "User has received a message"
            elif ",video" in string:
                return "User has received a video"
            elif ",image,status" in string:
                return "User has received a contact status update"
            elif ",image" in string:
                return "User has received an image"
        elif ",chat,read" in string:
            return "User has read a message"
        elif ",msgs,delete" in string:
            return "User has deleted a message"
        elif ",group,create" in string:
            return "User has created a group chat"
        elif ",block,true" in string:
            return "User has blocked a contact"
        elif ",pushname" in string:
            return "User has set a display name"
        elif ",status,set" in string:
            return "User has modified the 'about' information"
        elif ",set_pic" in string:
            return "User has set a probile picture"
        elif ",battery" in string:
            return "Current battery level of linked device"
    elif "mediaviewermodal:" in string:
        if "opened" in string:
            return "User opened the media viewer"
        elif "closed" in string:
            return "User closed the media viewer"
    elif "networkstatus online" in string:
        return "User is online"
    elif "call, ..." in string:
        return "User is on a call"
    elif "media:sendtochat" in string:
        return "User has sent a media file"
    elif "mediaload:video" in string:
        if not ".onerror" in string:
            return "User has accessed a video"
    
    return "?"