import net
import qqbot
from qqbot.model.message import MessageArk, MessageArkKv


async def service_get_city_weather(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    content = message.content
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
    msg_api = qqbot.AsyncMessageAPI(msg_api.token, msg_api.is_sandbox)
    await msg_api.post_message(message.channel_id, send)
