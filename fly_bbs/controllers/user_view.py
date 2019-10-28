 
from fly_bbs.extensions import mongo
import json
import datetime
from bson import ObjectId
from fly_bbs import utils
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from fly_bbs.models import User

user_view = Blueprint('user', __name__)

@user_view.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email_form = request.form.get('email')
        pwd_form = request.form.get('password')
        # ?????
        vercode = request.form.get('vercode')
        # ?????????
        utils.verify_num(vercode)
        user = mongo.db.users.find_one({'email': email_form})
        if not user:
            return jsonify({'status': 50102, 'msg': '?????'})
        if not User.validate_login(user['password'], pwd_form):
            return jsonify({'status': 'Error', 'msg': '????'})
        session['username'] = user['username']
        return redirect(url_for('index.index'))
    # ??????
    ver_code = utils.gen_verify_num()
    return render_template('user/login.html', ver_code=ver_code['question'])
    
@user_view.route('/register/')
def register():
    return render_template('user/reg.html') 
