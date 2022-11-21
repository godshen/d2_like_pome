import dao
from botpy.message import Message


async def activity_at_start(message: Message):
    dao.redis_activity_status_set("start")
    send = "抽奖开始啦！快艾特我参加抽奖吧！！\n"
    await message.reply(content=send)


async def activity_at_end(message: Message):
    dao.redis_activity_status_set("end")
    send = "抽奖结束\n"
    await message.reply(content=send)


async def activity_at_join(message: Message):
    uid = message.author.id
    is_started = dao.redis_activity_status_get()
    if is_started == "0":
        send = "活动尚未开始\n"
    else:
        dao.redis_activity_participate(uid)
        send = "<@%s>参加成功！\n" % uid
    await message.reply(content=send)


async def activity_get_result(message: Message):
    res = dao.redis_activity_get_result()
    send = "恭喜以下的同学获得活动的奖品哦ƪ(˘⌣˘)ʃ\n%s\n" % res
    await message.reply(content=send)

