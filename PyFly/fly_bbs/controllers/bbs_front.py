from flask import Blueprint, render_template

bbs_index = Blueprint("index", __name__)

@bbs_index.route('/')
def index():
    return render_template('base.html')
