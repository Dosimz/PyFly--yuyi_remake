import random
from flask import session, current_app
from flask_mail import Message
from . import extensions
from threading import Thread


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


# 设置接收者、发送内容等
def send_email(to, subject, body, is_txt=True):
    app = current_app._get_current_object()
    msg = Message(subject=app.config.get('MAIL_SUBJECT_PREFIX') + subject, sender=app.config.get('MAIL_USERNAME'), recipients=[to])
    if is_txt:
        msg.body = body
    else:
        msg.html = body
    # 多线程支持
    thr = Thread(target=send_mail_async, args=[app, msg])
    thr.start()
    return thr

# 发送邮件
def send_mail_async(app, msg):
    with app.app_context():
        extensions.mail.send(msg)
