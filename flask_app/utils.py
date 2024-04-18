from datetime import datetime

def current_time():
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')