import dao
import qqbot


async def service_manage(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    content = message.content
    msg_list = content.split(" ")
    if len(msg_list) == 2:
        send = qqbot.MessageSendRequest("侬行组撒", message.id)
        await msg_api.post_message(message.channel_id, send)
    else:
        if "排行榜" in msg_list[2]:
            send = qqbot.MessageSendRequest("第%d名:\t<@%s>" % (1, "12765512432620307406"), message.id)
            await msg_api.post_message(message.channel_id, send)
        elif "第一名" in msg_list[2]:
            send = qqbot.MessageSendRequest("必然是<@%s>" % "12765512432620307406", message.id)
            await msg_api.post_message(message.channel_id, send)
        else:
            send = qqbot.MessageSendRequest(msg_list[2], message.id)
            await msg_api.post_message(message.channel_id, send)


async def service_manage_err(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    send = qqbot.MessageSendRequest("暗号对接失败", message.id)
    await msg_api.post_message(message.channel_id, send)


def managers():
    return dao.get_managers_list()
