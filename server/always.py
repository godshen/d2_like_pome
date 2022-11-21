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
    get_username(None, None)
    return 0
