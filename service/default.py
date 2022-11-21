import dao
from botpy.message import Message


async def service_default(message: Message):
    send = "试试看输入:\n\t[/天气 城市名]\n\t[/签到]\n\t[/查询]\n\t[/抽签]\n\t[/解签]\n"
    await message.reply(content=send)


async def service_word_config(message: Message):
    content = message.content
    if "早安" in content:
        send = "晚安"
    elif "晚安" in content:
        send = "午安"
    elif "午安" in content:
        send = "早安"
    elif "揍圈圈" in content:
        send = "<@%s>揍你" % "12765512432620307406"
    else:
        send = "啊咧？"

    await message.reply(content=send)
