import os
import dao
import net


def init_service():
    appid = os.environ['QQ_ROBOT_APPID_STAND']
    token = os.environ['QQ_ROBOT_TOKEN_STAND']
    dao.init_dao()
    net.init_net()

    return appid, token
