import random
from flask import session

def verify_num(code):
    from .code_msg import VERIFY_CODE_ERROR

    if code != session['ver_code']:
        raise models.GlobalApiException(VERIFY_CODE_ERROR)
    # return result


def gen_verify_num():
    a = random.randint(-20, 20)
    b = random.randint(0, 50)
    data = {'question': str(a) + ' + ' + str(b) + " = ?", 'answer': str(a + b)}
    session['ver_code'] = data['answer']
    return data
