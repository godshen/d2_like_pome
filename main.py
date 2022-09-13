# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import qqbot
from qqbot.core.util import logging

import service
import server

logger = logging.getLogger()


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    logger.info("[%d] uid: %s, uname: %s, cmd: %s" %
                (int(time.time()), message.author.id, message.author.username, message.content)
                )
    # 根据指令触发不同的推送消息
    content_arr = message.content.split(" ")
    msg_api = qqbot.AsyncMessageAPI(t_token, is_test)

    await service.service_word_config(msg_api, message)

    content = ""
    if len(content_arr) >= 2:
        content = content_arr[1]

    if "/天气" == content:
        await service.service_get_city_weather(msg_api, message)
    elif "/签到" == content:
        await service.service_user_do_sign(msg_api, message)
        await service.service_get_sign_info(msg_api, message)
    elif "/图片" == content:
        await service.service_get_sign_picture(msg_api, message)
    elif "/补签" == content:
        await service.service_user_re_sign(msg_api, message)
    elif "/查询" == content:
        await service.service_get_sign_info(msg_api, message, True)
    elif "/抽奖" == content:
        await service.activity_at_join(msg_api, message)
    elif "/抽奖结果" == content:
        await service.activity_get_result(msg_api, message)
    elif "/开始抽奖" == content:
        if message.author.id in service.managers():
            await service.activity_at_start(msg_api, message)
        else:
            await service.service_manage_err(msg_api, message)
    elif "/结束抽奖" == content:
        if message.author.id in service.managers():
            await service.activity_at_end(msg_api, message)
        else:
            await service.service_manage_err(msg_api, message)
    elif "/管理" == content:
        if message.author.id in service.managers():
            await service.service_manage(msg_api, message)
        else:
            await service.service_manage_err(msg_api, message)
    else:
        await service.service_default(msg_api, message)


if __name__ == "__main__":
    print("sjzez great forever")

    t_token, is_test = server.init_project()

    service.init_service()

    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, is_test, qqbot_handler)
