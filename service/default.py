import dao
import qqbot


async def service_default(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    send = qqbot.MessageSendRequest("试试看输入:\n\t[/天气 城市名]\n\t[/签到]\n\t[/查询]\n", message.id)
    await msg_api.post_message(message.channel_id, send)


async def service_word_config(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    content = message.content
    if "早安" in content:
        send = qqbot.MessageSendRequest("晚安", message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "晚安" in content:
        send = qqbot.MessageSendRequest("午安", message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "午安" in content:
        send = qqbot.MessageSendRequest("早安", message.id)
        await msg_api.post_message(message.channel_id, send)
    elif "揍圈圈" in content:
        send = qqbot.MessageSendRequest("<@%s>揍你" % "12765512432620307406", message.id)
        await msg_api.post_message(message.channel_id, send)
