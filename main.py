# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import asyncio

import qqbot
from qqbot.core.util import logging
from qqbot.model.message import MessageArk, MessageArkKv

import dao
import net


logger = logging.getLogger()


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    # 根据指令触发不同的推送消息
    content = message.content
    msg_api = qqbot.AsyncMessageAPI(t_token, is_test)

    if "早安" in content:
        send = qqbot.MessageSendRequest("晚安", message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "晚安" in content:
        send = qqbot.MessageSendRequest("午安", message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "午安" in content:
        send = qqbot.MessageSendRequest("早安", message.id)
        await msg_api.post_message(message.channel_id, send)

    if "/天气" in content:
        # 通过空格区分城市参数
        split = content.split("/天气 ")
        weather = await net.get_weather(split[1])
        # 构造消息发送请求数据对象
        ark = MessageArk()
        # 模版ID=23
        ark.template_id = 23
        ark.kv = [
            MessageArkKv(key="#DESC#", value="描述"),
            MessageArkKv(key="#PROMPT#", value="提示消息"),
            MessageArkKv(key="#LIST#", obj=await net.create_ark_obj_list(weather))
        ]
        # 通过api发送回复消息
        send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message.id)
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        await msg_api.post_message(message.channel_id, send)
    elif "/签到" in content:
        try:
            user_id = message.author.id
            if dao.check_is_signed(user_id) != 0:
                send = qqbot.MessageSendRequest("<@%s>今天已经签到过了呢(灬°ω°灬) " % message.author.id, message.id)
            else:
                sign_reward = "积分"
                sign_type = 1
                sign_guild = message.guild_id
                sign_channel = message.channel_id
                dao.user_sign(user_id, sign_reward, sign_type, "", sign_guild, sign_channel)
                auto_id = dao.check_is_continuous(user_id)
                if auto_id != 0:
                    dao.update_continuous_days(auto_id)
                else:
                    dao.insert_continuous_beginning(user_id)
                send = qqbot.MessageSendRequest("<@%s>签到成功 " % message.author.id, message.id)
        except:
            send = qqbot.MessageSendRequest("<@%s>签到失败 " % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "/补签" in content:
        '''
        user_id = message.author.id
        sign_reward = "积分"
        sign_type = 2
        sign_guild = message.guild_id
        sign_channel = message.channel_id
        sign_time = content.split("/补签 ")
        if len(sign_time) == 2:
            user_sign(user_id, sign_reward, sign_type, sign_time[1], sign_guild, sign_channel)
            send = qqbot.MessageSendRequest("<@%s>补签成功 " % message.author.id, message.id)
        else:
            send = qqbot.MessageSendRequest("<@%s>补签出了点问题 " % message.author.id, message.id)
        '''
        send = qqbot.MessageSendRequest("<@%s>余额不足 " % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "/查询" in content:
        try:
            user_id = message.author.id
            _, cnt_days = dao.get_sign_info(user_id)
            continuous_days = dao.get_continuous_days(user_id)
            send = qqbot.MessageSendRequest("<@%s>签到天数: %d, 连续签到天数: %d" % (user_id, cnt_days, continuous_days), message.id)
        except:
            send = qqbot.MessageSendRequest("<@%s>签到失败" % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    else:
        send = qqbot.MessageSendRequest("试试看输入:\n\t[/天气 城市名]\n\t[/签到]\n\t[/查询]\n", message.id)
        await msg_api.post_message(message.channel_id, send)


def get_username():
    api = qqbot.AsyncUserAPI(t_token, is_test)
    loop = asyncio.get_event_loop()
    user = loop.run_until_complete(api.me())
    print(user.username)

    return 0


if __name__ == "__main__":
    print("project of qq-bot of d2_pome")
    is_test = False

    now_dir = os.path.abspath(os.path.dirname(__file__))
    os.environ['SSL_CERT_FILE'] = now_dir + "/config/qq-bot-cert.pem"

    appid_str = os.environ['QQ_ROBOT_APPID']  # always be "102006831"
    token_str = os.environ['QQ_ROBOT_TOKEN']  # just like "NvM0ZVRsamsPrpK61wzdcmbeK0maPSIj"
    t_token = qqbot.Token(appid_str, token_str)

    get_username()

    db_host = os.environ['ROBOT_DB_HOST']
    dao.RobotData(db_host, 3306, 'develop', 'Sjzez=19480913', 'robot', 600)

    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, is_test, qqbot_handler)
