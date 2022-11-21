import net
from botpy.message import Message
from botpy.types.message import Ark, ArkKv


async def service_get_city_weather(message: Message):
    content = message.content
    # 通过空格区分城市参数
    split = content.split("/天气 ")
    weather = await net.get_weather(split[1])
    # 构造消息发送请求数据对象
    payload: Ark = Ark(
        template_id=23,
        kv=[
            ArkKv(key="#DESC#", value="描述"),
            ArkKv(key="#PROMPT#", value="提示消息"),
            ArkKv(key="#LIST#", obj=await net.create_ark_obj_list(weather))
        ],
    )

    # 通过api发送回复消息
    await message.reply(ark=payload)
