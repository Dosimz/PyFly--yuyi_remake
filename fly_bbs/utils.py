import random
from flask import session

# ?????
def verify_num(code):
    if code != session['ver_code']:
        raise Exception('??????')

# ?????
def gen_verify_num():
    a = random.randint(-20, 20)
    b = random.randint(0, 50)
    data = {'question': str(a) + ' + ' + str(b) + " = ?", 'answer': str(a + b)}
    session['ver_code'] = data['answer']
    return data