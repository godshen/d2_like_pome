import os
import qqbot
import asyncio


def get_username(t_token, is_test):
    api = qqbot.AsyncUserAPI(t_token, is_test)
    loop = asyncio.get_event_loop()
    user = loop.run_until_complete(api.me())
    print(user.username)

    return 0


def init_project():
    is_test = False
    now_dir = os.path.abspath(os.path.dirname(__file__))
    # os.environ['SSL_CERT_FILE'] = now_dir + "/config/qq-bot-cert.pem"
    appid_str = os.environ['QQ_ROBOT_APPID']  # always be "102006831"
    token_str = os.environ['QQ_ROBOT_TOKEN']  # just like "NvM0ZVRsamsPrpK61wzdcmbeK0maPSIj"
    t_token = qqbot.Token(appid_str, token_str)
    get_username(t_token, is_test)
    return t_token, is_test
