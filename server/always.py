import service

import botpy
from botpy.message import Message
from botpy import logging

import time

_log = logging.get_logger()


class D2LikePome(botpy.Client):
    async def on_at_message_create(self, message: Message):
        _log.info("[%d] uid: %s, uname: %s, cmd: %s" % (
            int(time.time()), message.author.id, message.author.username, message.content)
        )

        # 先发送消息告知用户
        # await self.api.post_message(message.channel_id, content="command received: %s" % message.content)

        content = ""
        content_arr = message.content.split(" ")

        if len(content_arr) >= 2:
            content = content_arr[1]
        _log.info(content)

        if "/天气" == content:
            await service.service_get_city_weather(message)

        elif "/签到" == content:
            await service.service_user_do_sign(message)
            await service.service_get_sign_info(message)

        elif "/抽签" == content:
            await service.service_draw_get_one(message)

        elif "/解签" == content:
            await service.service_draw_solve_one(message)

        elif "/图片" == content:
            await service.service_get_sign_picture(message)

        elif "/补签" == content:
            await service.service_user_re_sign(message)

        elif "/查询" == content:
            await service.service_get_sign_info(message, True)

        elif "/抽奖" == content:
            await service.activity_at_join(message)

        elif "/抽奖结果" == content:
            await service.activity_get_result(message)

        elif "/开始抽奖" == content:
            if message.author.id in service.managers():
                await service.activity_at_start(message)
            else:
                await service.service_manage_err(message)

        elif "/结束抽奖" == content:
            if message.author.id in service.managers():
                await service.activity_at_end(message)
            else:
                await service.service_manage_err(message)

        elif "/管理" == content:
            if message.author.id in service.managers():
                await service.service_manage(message)
            else:
                await service.service_manage_err(message)

        else:
            await service.service_default(message)


def init_project():
    a, t = service.init_service()
    intents = botpy.Intents(public_guild_messages=True)
    c = D2LikePome(intents=intents)
    return c, a, t


def run_project(c: D2LikePome, a, t):
    c.run(appid=a, token=t)
