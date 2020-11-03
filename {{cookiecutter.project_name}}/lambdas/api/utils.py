import json

def validate_method(event, method="GET", path="/"):
    if event.get('version') == "1.0" :
        request_method = event.get("httpMethod")
    else:
        request_method = event.get("http").get("method")

    if method != request_method:
        return False
    return True


def validate_path(event,  path="/"):
    if event.get('version') =="1.0":
        request_path = event.get("path")
    else:
        request_path = event.get("http").get("path")
        
    if path != request_path:
        return False
    return True