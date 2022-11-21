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
    is_test = True
    appid_str = os.environ['QQ_ROBOT_APPID_STAND']
    token_str = os.environ['QQ_ROBOT_APPID_STAND']
    # t_token = qqbot.Token(appid_str, token_str)
    # get_username(t_token, is_test)
    return is_test, appid_str, token_str
