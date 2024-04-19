from datetime import datetime

def current_time():
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

def get_duration(duration_ms, item):
    if item == 'album':
        duration_min = round(duration_ms / 1000 / 60)
        hours, minutes = duration_min // 60, duration_min % 60
        if hours == 0:
            return f'{minutes} min'
        else:
            return f'{hours} hr {minutes} min'
    else:
        duration_s = round(duration_ms / 1000)
        minutes, seconds = duration_s // 60, duration_s % 60
        return f"{minutes}:{str(seconds).zfill(2)}"