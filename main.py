import os
import json
import asyncio
import aiohttp
from typing import Dict, List

import qqbot
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv, MessageArkObj, MessageArkObjKv


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
        send = qqbot.MessageSendRequest("<@%s>签到成功 " % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "/查询" in content:
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        send = qqbot.MessageSendRequest("<@%s>查到了, 你就是大聪明！ " % message.author.id, message.id)
        await msg_api.post_message(message.channel_id, send)
    else:
        msg_api = qqbot.AsyncMessageAPI(t_token, is_test)
        send = qqbot.MessageSendRequest("<@%s--%s>你想干啥咧 " % (message.author.bot, message.author.avatar), message.id)
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
    is_test = True

    now_dir = os.path.abspath(os.path.dirname(__file__))
    os.environ['SSL_CERT_FILE'] = now_dir + "/config/qq-bot-cert.pem"

    appid_str = os.environ['QQ_ROBOT_APPID']  # always be "102006831"
    token_str = os.environ['QQ_ROBOT_TOKEN']  # just like "NvM0ZVRsamsPrpK61wzdcmbeK0maPSIj"
    t_token = qqbot.Token(appid_str, token_str)

    get_username()

    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, is_test, qqbot_handler)
