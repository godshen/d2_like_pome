import dao
import qqbot


async def activity_at_start(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    dao.redis_activity_status_set("start")
    send = qqbot.MessageSendRequest("抽奖开始啦！快艾特我参加抽奖吧！！\n", message.id)
    await msg_api.post_message(message.channel_id, send)


async def activity_at_end(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    dao.redis_activity_status_set("end")
    send = qqbot.MessageSendRequest("抽奖结束\n", message.id)
    await msg_api.post_message(message.channel_id, send)


async def activity_at_join(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    uid = message.author.id
    is_started = dao.redis_activity_status_get()
    if is_started == "0":
        send = qqbot.MessageSendRequest("活动尚未开始\n", message.id)
        await msg_api.post_message(message.channel_id, send)
    else:
        dao.redis_activity_participate(uid)
        send = qqbot.MessageSendRequest("<@%s>参加成功！\n" % uid, message.id)
        await msg_api.post_message(message.channel_id, send)


async def activity_get_result(msg_api: qqbot.AsyncMessageAPI, message: qqbot.Message):
    res = dao.redis_activity_get_result()
    send = qqbot.MessageSendRequest("恭喜以下的同学获得活动的奖品哦ƪ(˘⌣˘)ʃ\n%s\n" % res, message.id)
    await msg_api.post_message(message.channel_id, send)

