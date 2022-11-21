import os
import dao
import net


def ping_by_name():
    return 0


def init_service():
    appid = os.environ['QQ_ROBOT_APPID']
    token = os.environ['QQ_ROBOT_TOKEN']
    dao.init_dao()
    net.init_net()
    ping_by_name()
    return appid, token
