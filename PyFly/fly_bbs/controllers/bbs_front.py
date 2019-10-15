from flask import Blueprint, render_template, request, session, jsonify, url_for, redirect, flash
from fly_bbs import forms, utils, db_utils
from bson.objectid import ObjectId
from datetime import datetime
from fly_bbs.extensions import mongo
import pymongo
from flask_login import current_user

bbs_index = Blueprint("index", __name__)

# @bbs_index.route('/')
# def index():
#     if 'username' in session:
#         username = session['username']
#         print(username)
#     else:
#         username = None
#     return render_template('base.html', username=username)


@bbs_index.route('/')
@bbs_index.route('/page/<int:pn>/size/<int:size>')
@bbs_index.route('/page/<int:pn>')
@bbs_index.route("/catalog/<ObjectId:catalog_id>")
@bbs_index.route("/catalog/<ObjectId:catalog_id>/page/<int:pn>")
@bbs_index.route("/catalog/<ObjectId:catalog_id>/page/<int:pn>/size/<int:size>")
# @cache.cached(timeout=2 * 60, key_prefix=utils.gen_cache_key)
def index(pn=1, size=10, catalog_id=None):
    flash("asdsdsad")

    sort_key = request.values.get('sort_key', '_id')
    print(sort_key)
    sort_by = (sort_key, pymongo.DESCENDING)
    print(pymongo.DESCENDING)
    post_type = request.values.get('type')
    filter1 = {}
    if post_type == 'not_closed':
        filter1['is_closed'] = {'$ne': True}
    if post_type == 'is_closed':
        filter1['is_closed'] = True
    if post_type == 'is_cream':
        filter1['is_cream'] = True
    if catalog_id:
        filter1['catalog_id'] = catalog_id
    page = db_utils.get_page('posts', pn=pn, filter1=filter1, size=size, sort_by=sort_by)
    # print(page)
    return render_template("post_list.html", is_index=catalog_id is None, page=page, sort_key=sort_key, catalog_id=catalog_id, post_type=post_type)



@bbs_index.route('/add', methods=['GET', 'POST'])
@bbs_index.route('/edit/<ObjectId:post_id>', methods=['GET', 'POST'])
def add(post_id=None):
    posts_form = forms.PostsForm()
    if posts_form.is_submitted():
        if not posts_form.validate():
            return jsonify({'status': 50001, 'msg': str(posts_form.errors)})
        utils.verify_num(posts_form.vercode.data)
        # 用户权限控制
        user = current_user.user
        if not user.get('is_active', False) or user.get('is_disabled', False):
            # return jsonify(code_msg.USER_UN_ACTIVE_OR_DISABLED)
            return jsonify({'msg': '用户未激活或已被封杀'})
        # 用户金币权限控制
        user_coin = user.get('coin', 0)
        print(posts_form.reward.data)
        print(user_coin)
        print(request.form)
        if posts_form.reward.data > user_coin:
            # return jsonify(models.R.ok('悬赏金币不能大于拥有的金币，当前账号金币为：' + str(user_coin)))
            return jsonify({'msg': '悬赏金币不能大于拥有的金币，当前账号为； ' + str(user_coin)})
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
            # # 扣除用户发帖悬赏
            if reward > 0:
                mongo.db.users.update_one({'_id': user['_id']}, {'$inc': {'coin': -reward}})
            mongo.db.posts.save(posts)
            post_id = posts['_id']

        # 更新索引文档
        # update_index(mongo.db.posts.find_one_or_404({'_id': post_id}))

        return redirect(url_for('index.index'))
    else:
        ver_code = utils.gen_verify_num()
        # session['ver_code'] = ver_code['answer']
        posts = None
        if post_id:
            posts = mongo.db.posts.find_one_or_404({'_id': post_id})
        title = '发帖' if post_id is None else '编辑帖子'
        return render_template('jie/add.html', page_name='jie', ver_code=ver_code['question'], form=posts_form, is_add=(post_id is None), post=posts, title=title)


# 帖子详情页
@bbs_index.route('/post/<ObjectId:post_id>/')
@bbs_index.route('/post/<ObjectId:post_id>/page/<int:pn>/')
def post_detail(post_id, pn=1):
    post = mongo.db.posts.find_one_or_404({'_id': post_id})
    if post:
        post['view_count'] = post.get('view_count', 0) + 1
        mongo.db.posts.save(post)
    post['user'] = db_utils.find_one('users', {'_id': post['user_id']}) or {}
    # 获取评论
    page = db_utils.get_page('comments', pn=pn, size=10, filter1={'post_id': post_id}, sort_by=('is_adopted', -1))
    return render_template('jie/detail.html', post=post, title=post['title'], page_name='jie', comment_page=page, catalog_id=post['catalog_id'])
