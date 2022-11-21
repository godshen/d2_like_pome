import dao
from botpy.message import Message


async def service_manage(message: Message):
    content = message.content
    msg_list = content.split(" ")
    if len(msg_list) == 2:
        send = "侬行组撒\n"
    else:
        if "排行榜" in msg_list[2]:
            send = "第%d名:\t<@%s>" % (1, "12765512432620307406")
        elif "第一名" in msg_list[2]:
            send = "必然是<@%s>" % "12765512432620307406"
        else:
            send = msg_list[2]

    await message.reply(content=send)


async def service_manage_err(message: Message):
    send = "暗号对接失败"
    await message.reply(content=send)


def managers():
    return dao.get_managers_list()
