from flask import Blueprint, render_template, session

bbs_index = Blueprint("index", __name__)

@bbs_index.route('/')
def index():
    if 'username' in session:
        username = session['username']
        print(username)
    else:
        user = None
    return render_template('base.html', username=username)
