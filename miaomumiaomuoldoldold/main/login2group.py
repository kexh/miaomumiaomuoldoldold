from process.login_qq import Login
from process.rec_msg import RecMsg
from process.send_qg_msg import SendMsg
def main():
    lg = Login()
    cookies = lg.login_main()

    user_id = None

    r = RecMsg()
    while True:
        msg = r.rec_msg()
        if msg != None:
            print msg
            msg = '123' #  先不要跟上面返回一样
            s = SendMsg()
            if s.send_msg(user_id, msg):
                print 'hahaha'

if __name__ == '__main__':
    main()