from miaomu_robot.nlp import nlp
from miaomu_robot.qq_process.login_qq import Login
from miaomu_robot.qq_process.rec_msg import RecMsg
from miaomu_robot.qq_process.send_qgroup_msg import SendMsg


def group_chat():
    lg = Login()
    cookies = lg.login_main()

    user_id = None

    r = RecMsg()
    while True:
        msg = r.rec_msg()
        if msg != None:
            print msg
            ans = nlp(msg)
            s = SendMsg()
            if s.send_msg(user_id, ans):
                print 'send msg success. '

if __name__ == '__main__':
    group_chat()


