from fly_bbs.extensions import mongo
from bson.objectid import ObjectId
from fly_bbs.models import Page

def get_page(collection_name, pn=1, size=10, sort_by=None, filter1=None):
    _process_filter(filter1)
    if size <= 0:
        size = 15
    # 查询 collection_name 集合的符合 filter1 条件的所有内容
    total = mongo.db[collection_name].count(filter1)
    # print(total)
    # 计算要跳过多少数量的数据
    skip_num = (pn - 1) * size
    result = []
    # 表示帖子内容是否全部展示完
    has_more = total > pn * size
    if total - skip_num > 0:
        # 查找数据
        result = mongo.db[collection_name].find(filter1, limit=size)
        # 按顺序排列
        if sort_by:
            result = result.sort(sort_by[0], sort_by[1])

        if skip_num >= 0:
            # 使用 skip 方法跳过指定数量的数据
            result.skip(skip_num)
    # 计算出总页数
    total_page = int(total / size)
    if total % size > 0:
        total_page = total_page + 1
    
    page = Page(pn, size, sort_by, filter1, list(result), has_more, total_page, total)
    return page


def get_option(name, default=None):
    return mongo.db.options.find_one({'code': name}) or default


def _process_filter(filter1):
    if filter1 is None:
        return
    _id = filter1.get('_id')
    if _id and not isinstance(_id, ObjectId):
        filter1['_id'] = ObjectId(_id)


def get_list(collection_name, sort_by=None, filter1=None, size=None):
    _process_filter(filter1)
    result = mongo.db[collection_name].find(filter1)
    if sort_by:
        result = result.sort(sort_by[0], sort_by[1])
    if size:
        result = result.limit(size)
    result = list(result)
    return result


def find_one(collection_name, filter1=None):
    _process_filter(filter1)
    return mongo.db[collection_name].find_one(filter1)