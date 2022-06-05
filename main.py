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
    content = message.content
    msg_api = qqbot.AsyncMessageAPI(t_token, is_test)

    await service.service_word_config(msg_api, message)

    if "/天气" in content:
        await service.service_get_city_weather(msg_api, message)
    elif "/签到" in content:
        await service.service_user_do_sign(msg_api, message)
    elif "/打卡" in content:
        await service.service_user_do_sign(msg_api, message)
    elif "/sign" in content:
        await service.service_user_do_sign(msg_api, message)
    elif "/补签" in content:
        await service.service_user_re_sign(msg_api, message)
    elif "/查询" in content:
        await service.service_get_sign_info(msg_api, message)
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
