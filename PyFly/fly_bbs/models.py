from werkzeug.security import check_password_hash
from json import JSONEncoder

class Page:
    def __init__(self, pn, size, sort_by=None, filter1=None, result=None, has_more=False, total_page=0, total=0):
        self.pn = pn
        self.size = size
        self.sort_by = sort_by
        self.result = result
        self.filter1 = filter1
        self.has_more = has_more
        self.total_page = total_page
        self.total=total

    def __repr__(self):
        return JSONEncoder().encode(o = self.__dict__)


class User:
    user = None
    # is_active = False
    # is_authenticated = True
    # is_anonymous = False
    
    def __init__(self, user):
        self.user = user
        # self.is_active = user['is_active']
        # self.is_active = False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.user['is_active']

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.user['_id'])

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

