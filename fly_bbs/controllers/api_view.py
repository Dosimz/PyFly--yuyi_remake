from flask import Blueprint, render_template,flash, request,session,jsonify, url_for, current_app, redirect, abort
from flask_login import login_user, logout_user, login_required, current_user

from fly_bbs import db_utils, forms, models, code_msg
from fly_bbs.extensions import mongo
from bson.objectid import ObjectId
# from bson.json_util import dumps
from datetime import datetime
import random

api_view = Blueprint("api", __name__, url_prefix="", template_folder="templates")

@api_view.route('/post/delete/<ObjectId:post_id>', methods=['POST'])
@login_required

def post_delete(post_id):
    post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
    # 只有帖子的发布者和管理员可以删除帖子
    if post['user_id'] != current_user.user['_id'] and not current_user.user['is_admin']:
        return jsonify(code_msg.USER_UN_HAD_PERMISSION)
    # 删除帖子
    mongo.db.posts.delete_one({'_id': post_id})
    # 删除帖子其他用户收藏夹中的 post_id
    mongo.db.users.update_many({}, {'$pull': {'collections': post_id}})
    # 删除检索索引
    # whoosh_searcher.delete_document('posts', 'obj_id', str(post_id))

    return jsonify(code_msg.DELETE_SUCCESS.put('action', url_for('index.index', catalog_id=post['catalog_id'])))


@api_view.route('/post/set/<ObjectId:post_id>/<string:field>/<int:val>', methods=['POST'])
@login_required
def post_set(post_id, field, val):
    post = mongo.db.posts.find_one_or_404({'_id': post_id})
    catalog = mongo.db.catalogs.find_one_or_404({'_id': post['catalog_id']})
    if field != 'is_closed':
        if not current_user.user['is_admin'] and current_user.user['_id'] != catalog['moderator_id']:
            return jsonify(code_msg.USER_UN_HAD_PERMISSION)
    elif current_user.user['_id'] != post['user_id'] and not current_user.user['is_admin']\
            and current_user.user['_id'] != catalog['moderator_id']:
        return jsonify(code_msg.USER_UN_HAD_PERMISSION)
    val = val == 1
    # 更新帖子状态
    mongo.db.posts.update_one({'_id': post_id}, {'$set': {field: val}})
    return jsonify(models.R.ok())