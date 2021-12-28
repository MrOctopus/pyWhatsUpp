# See https://www.semanticscholar.org/paper/Browser-Forensic-Investigations-of-WhatsApp-Web-Paligu-Varol/0054508526255eff5c15de5ab3194591e842d731
def get_event_type(string):
    string = string.lower()

    if "action," in string:
        if "message,chat" in string:
            if "send:" in string:
                return "User sent a message"
        elif "msg,relay,chat" in string:
            if "recv: " in string:
                return "User received a message"
        elif "presence,unavailable" in string:
            return "User is unavailable"
        elif "presence,available" in string:
            return "User is available"
    elif "mediaviewermodal:" in string:
        if "opened" in string:
            return "User opened the media viewer"
        elif "closed" in string:
            return "User closed the media viewer"
    elif "networkstatus online" in string:
        return "User is online"
    elif "call, ..." in string:
        return "User is on a call"
    elif "mediaload:video" in string:
        if not ".onerror" in string:
            return "User has accessed a video"
    
    return "?"