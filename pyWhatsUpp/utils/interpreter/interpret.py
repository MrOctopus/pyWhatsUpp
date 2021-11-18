def get_event_type(string):
    string = string.lower()

    if "action,message,chat" in string:
        if "send:" in string:
            return "User sent a message"
    elif "action,msg,relay,chat" in string:
        if "recv: " in string:
            return "User received a message"
    elif "networkstatus online" in string:
        return "User is online"
    elif "action,presence,unavailable" in string:
        return "User is unavailable"
    elif "action,presence,available" in string:
        return "User is available"
    elif "call, ..." in string:
        return "User is on a call"
    elif "video.onloadeddata" in string:
        return "User has accessed a video"
    
    return "?"