# See https://www.semanticscholar.org/paper/Browser-Forensic-Investigations-of-WhatsApp-Web-Paligu-Varol/0054508526255eff5c15de5ab3194591e842d731
# See https://hammer.purdue.edu/articles/thesis/WhatsApp_Forensics_Locating_Artifacts_in_Web_and_Desktop_Clients/8029109/files/14954516.pdf

# NOTE: This is a very, VERY inefficient way of doing interpretation.
# There are way better ways of doing this, but it works for now as POC.
# Example of improving the speed drastically: Token parsing
def get_event_type(event):
    event = event.lower()
    
    if "action," in event:
        if ",presence" in event:
            if ",available" in event:
                return "User is available"
            elif ",unavailable" in event:
                return "User is unavailable"
        if ",chatstate" in event:
            if ",composing" in event:
                return "User is typing a message"
            elif ",paused" in event:
                return "User has stopped typing a message"
        elif "message" in event:
            if ",image" in event:
                return "User has sent an image"
            elif ",video" in event:
                return "User has sent a video"
            elif ",chat" in event:
                return "User has sent a message"
            elif ",vcard" in event:
                return "User has sent contact information"
            elif ",document" in event:
                return "User has sent a document"
            elif ",ptt" in event:
                return "User has sent an audio message"
        elif ",msg,relay" in event:
            if ",chat" in event:
                return "User has received a message"
            elif ",video" in event:
                return "User has received a video"
            elif ",image,status" in event:
                return "User has received a contact status update"
            elif ",image" in event:
                return "User has received an image"
        elif ",chat,read" in event:
            return "User has read a message"
        elif ",msgs,delete" in event:
            return "User has deleted a message"
        elif ",group,create" in event:
            return "User has created a group chat"
        elif ",block,true" in event:
            return "User has blocked a contact"
        elif ",pushname" in event:
            return "User has set a display name"
        elif ",status,set" in event:
            return "User has modified the 'about' information"
        elif ",set_pic" in event:
            return "User has set a probile picture"
        elif ",battery" in event:
            return "Current battery level of linked device"
    elif "mediaviewermodal:" in event:
        if "opened" in event:
            return "User opened the media viewer"
        elif "closed" in event:
            return "User closed the media viewer"
    elif "networkstatus online" in event:
        return "User is online"
    elif "call, ..." in event:
        return "User is on a call"
    elif "media:sendtochat" in event:
        return "User has sent a media file"
    elif "mediaload:video" in event:
        if not ".onerror" in event:
            return "User has accessed a video"
    
    return "?"