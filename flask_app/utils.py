from datetime import datetime
from flask import render_template

def current_time():
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

def custom_404(e):
    return render_template('404.html', error=str(e)), 404