from flask import Blueprint, render_template,flash, request, url_for, current_app, session, jsonify, abort, redirect
from fly_bbs import db_utils, utils, forms, models, code_msg
from fly_bbs.extensions import mongo
from flask_login import login_required
from flask_login import current_user
from bson.objectid import ObjectId
import pymongo
from datetime import datetime

bbs_index = Blueprint("index", __name__)

@bbs_index.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('base.html', username=username)


@bbs_index.route('/add', methods=['GET', 'POST'])
@bbs_index.route('/edit/<ObjectId:post_id>', methods=['GET', 'POST'])
def add(post_id=None):
    posts_form = forms.PostsForm()
    if posts_form.is_submitted():
        if not posts_form.validate():
            return jsonify(models.BaseResult(1, str(posts_form.errors)))
        utils.verify_num(posts_form.vercode.data)
        # 拿到已登录用户信息
        user = current_user.user
        if not user.get('is_active', False) or user.get('is_disabled', False):
            return jsonify(code_msg.USER_UN_ACTIVE_OR_DISABLED)
        # 拿到用户拥有的金币数量
        user_coin = user.get('coin', 0)
        if posts_form.reward.data > user_coin:
            return jsonify(models.R.ok('悬赏金币不能大于拥有的金币，当前账号为：' + str(user_coin)))
        # 帖子信息
        posts = {
            'title': posts_form.title.data,
            'catalog_id': ObjectId(posts_form.catalog_id.data),
            'is_closed': False,
            'content': posts_form.content.data,
        }

        post_index = posts.copy()
        post_index['catalog_id'] = str(posts['catalog_id'])

        msg = '发帖成功！'
        reward = posts_form.reward.data
        if post_id:
            posts['modify_at'] = datetime.now()
            mongo.db.posts.update_one({'_id': post_id}, {'$set': posts})
            msg = '修改成功！'

        else:
            posts['create_at'] = datetime.utcnow()
            posts['reward'] = reward
            posts['user_id'] = user['_id']
            # 扣除发帖消耗的悬赏
            if reward > 0:
                mongo.db.users.update_one({'_id': user['_id']}, {'$inc': {'coin': -reward}})
            mongo.db.posts.save(posts)
            post_id = posts['_id']
        # action 会传入 js 部分中触发页面跳转
        return jsonify(models.R.ok(msg).put('action', url_for('index.index')))
    else:
        ver_code = utils.gen_verify_num()
        posts = None
        if post_id:
            posts = mongo.db.posts.find_one_or_404({'_id': post_id})
        title = '发帖' if post_id is None else '编辑帖子'
        return render_template('jie/add.html', page_name='jie', ver_code=ver_code['question'], form=posts_form, is_add=(post_id is None), post=posts, title=title)
