# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import asyncio
import aiohttp
import datetime
from typing import Dict, List

import qqbot
from qqbot.core.util import logging
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv, MessageArkObj, MessageArkObjKv

from dao import RobotData


logger = logging.getLogger()


async def get_weather(city_name: str) -> Dict:
    """
    获取天气信息
    :return: 返回天气数据的json对象
    """
    weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + \
                      city_name + \
                      "&appkey=%s&sign=%s&format=%s" % \
                      ("10003", "b59bc3ef6191eb9f747dd4e83c99f2a4", "json")
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj


def check_is_signed(user_id):
    sql = "select count(1) from `user_sign_log` where true and "
    time_today = datetime.date.today()
    condition = "`user_id`='%s' and date_format(`sign_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_today)
    cnt = db_mysql.do_select_cnt(sql + condition)
    return cnt


def get_continuous_days(user_id):
    sql = "select `days` from `user_continuous_sign` where true and "
    time_today = datetime.date.today()
    condition = "`user_id`='%s' and date_format(`update_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_today)
    lines = db_mysql.do_select(sql + condition)
    if len(lines) == 0:
        days = 0
    else:
        days = lines[0][0]
    return days


def check_is_continuous(user_id):
    sql = "select `id` from `user_continuous_sign` where true and "
    time_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    condition = "`user_id`='%s' and date_format(`update_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_yesterday)
    lines = db_mysql.do_select(sql + condition)
    if len(lines) == 0:
        auto_id = 0
    else:
        auto_id = lines[0][0]
    return auto_id


def insert_continuous_beginning(user_id):
    sql = "insert into `user_continuous_sign`(`user_id`, `days`) values(%s,%s)"
    val = (user_id, 1)
    db_mysql.do_insert(sql, val)
    return 0


def update_continuous_days(id):
    sql = "update `user_continuous_sign` set `days`=`days`+1 where `id`=%s"
    val = (id)
    db_mysql.do_update(sql, val)
    return 0


def user_sign(user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel):
    if sign_time == "":
        sign_time_fmt = datetime.datetime.now()
    else:
        sign_time_fmt = datetime.datetime.strptime(sign_time+" 12:00:00", "%Y-%m-%d %H:%M:%S")
    _do_insert_sign_data(user_id, sign_reward, sign_type, sign_time_fmt, sign_guild, sign_channel)


def _do_insert_sign_data(user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel):
    sql = "insert into `user_sign_log`(`user_id`, `sign_reward`, `sign_type`, `sign_time`, `sign_guild`, `sign_channel`) values(%s,%s,%s,%s,%s,%s)"
    val = (user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel)
    db_mysql.do_insert(sql, val)


def get_sign_info(user_id):
    sql = "select count(1)c0, count(distinct date_format(`sign_time`,'%Y-%m-%d'))c1 from `user_sign_log` where true and "
    condition = "`user_id`='%s'" % user_id
    ret_data = db_mysql.do_select(sql + condition)[0]
    cnt_all = ret_data[0]
    cnt_day = ret_data[1]
    return cnt_all, cnt_day


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    # 根据指令触发不同的推送消息
    content = message.content
    if "/天气" in content:
        # 通过空格区分城市参数
        split = content.split("/天气 ")
        weather = await get_weather(split[1])
        await send_weather_ark_message(weather, message.channel_id, message.id)
    elif "/签到" in content:
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        try:
            user_id = message.author.id
            if check_is_signed(user_id) != 0:
                send = qqbot.MessageSendRequest("<@%s>今天已经签到过了嗷 " % message.author.id, message.id)
            else:
                sign_reward = "积分"
                sign_type = 1
                sign_guild = message.guild_id
                sign_channel = message.channel_id
                user_sign(user_id, sign_reward, sign_type, "", sign_guild, sign_channel)
                auto_id = check_is_continuous(user_id)
                if auto_id != 0:
                    update_continuous_days(auto_id)
                else:
                    insert_continuous_beginning(user_id)
                send = qqbot.MessageSendRequest("<@%s>签到成功 " % message.author.id, message.id)
        except:
            send = qqbot.MessageSendRequest("<@%s>签到失败 " % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "/补签" in content:
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
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
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        try:
            user_id = message.author.id
            _, cnt_days = get_sign_info(user_id)
            continuous_days = get_continuous_days(user_id)
            send = qqbot.MessageSendRequest("<@%s>签到天数: %d, 连续签到天数: %d" % (user_id, cnt_days, continuous_days), message.id)
        except:
            send = qqbot.MessageSendRequest("<@%s>签到失败" % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    else:
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        send = qqbot.MessageSendRequest("试试看输入:\n\t\t[/天气 城市名]\n\t\t[/签到]\n\t\t[/查询]\n", message.id)
        await msg_api.post_message(message.channel_id, send)


async def _create_ark_obj_list(weather_dict) -> List[MessageArkObj]:
    obj_list = [
        MessageArkObj(obj_kv=[
            MessageArkObjKv(key="desc", value=
                            weather_dict['result']['citynm'] + " " +
                            weather_dict['result']['weather'] + " " +
                            weather_dict['result']['days'] + " " +
                            weather_dict['result']['week'])
            ]
        ),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当日温度区间：" + weather_dict['result']['temperature'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前温度：" + weather_dict['result']['temperature_curr'])]),
        MessageArkObj(obj_kv=[MessageArkObjKv(key="desc", value="当前湿度：" + weather_dict['result']['humidity'])])
    ]
    return obj_list


async def send_weather_ark_message(weather_dict, channel_id, message_id):
    """
    被动回复-子频道推送模版消息
    :param channel_id: 回复消息的子频道ID
    :param message_id: 回复消息ID
    :param weather_dict:天气消息
    """
    # 构造消息发送请求数据对象
    ark = MessageArk()
    # 模版ID=23
    ark.template_id = 23
    ark.kv = [
        MessageArkKv(key="#DESC#", value="描述"),
        MessageArkKv(key="#PROMPT#", value="提示消息"),
        MessageArkKv(key="#LIST#", obj=await _create_ark_obj_list(weather_dict))
    ]
    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=message_id)
    msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
    await msg_api.post_message(channel_id, send)


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
    db_mysql = RobotData(db_host, 3306, 'develop', 'Sjzez=19480913', 'robot', 600)

    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, is_test, qqbot_handler)
