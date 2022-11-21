import dao
import pic
from botpy.message import Message
import random


async def service_user_do_sign(message: Message):
    try:
        success_words = [
            "签到成功啦୧(﹒︠ᴗ﹒︡)୨",
            "好耶！积分喜加一！(〃'▽'〃)",
            "成功啦！明天也不要忘记哦(〃'▽'〃)"
        ]
        user_id = message.author.id
        if dao.check_is_signed(user_id) != 0:
            send = "<@%s>今天已经签到过了呢(灬°ω°灬) " % message.author.id
        else:
            sign_reward = "积分"
            sign_type = 1
            sign_guild = message.guild_id
            sign_channel = message.channel_id
            dao.user_sign(user_id, sign_reward, sign_type, "", sign_guild, sign_channel)
            auto_id = dao.check_is_continuous(user_id)
            if auto_id != 0:
                dao.update_continuous_days(auto_id)
            else:
                dao.insert_continuous_beginning(user_id)
            send = "<@%s>%s " % (message.author.id, random.choice(success_words))
    except:
        send = "<@%s>签到失败 " % message.author.id
    await message.reply(content=send)


async def service_user_re_sign(message: Message):
    """
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
    """
    send = "<@%s>余额不足 " % message.author.id
    await message.reply(content=send)


async def service_get_sign_info(message: Message, need_detail=False):
    try:
        user_id = message.author.id
        _, cnt_days, points, details = dao.get_sign_info(user_id)
        continuous_days = dao.get_continuous_days(user_id)
        pic_url = ""
        if need_detail:
            send = "<@%s>你的签到详情如下:\n" \
                   "\t目前积分: %5d分\n\t基础天数: %5d天\n" \
                   "\t连续%2d天次数:\t%3d次\n\t连续%2d天次数:\t%3d次\n" \
                   "\t连续%2d天次数:\t%3d次\n\t连续%2d天次数:\t%3d次\n" % \
                   (user_id, points, cnt_days, 30, details[0], 15, details[1], 7, details[2], 3, details[3])
        else:
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            pic_name = pic.generata_pic(cnt_days, continuous_days, points, today + "-" + user_id)
            send = "<@%s>你的签到信息如下:" % message.author.id
            pic_url = "https://www.d2robot.site/image/" + pic_name
    except:
        pic_url = ""
        send = "<@%s>查询失败" % message.author.id
    await message.reply(content=send, pic_url=pic_url)


async def service_get_sign_picture(message: Message, need_detail=False):
    user_id = message.author.id
    _, cnt_days, points, details = dao.get_sign_info(user_id)
    continuous_days = dao.get_continuous_days(user_id)
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    pic_name = pic.generata_pic(cnt_days, continuous_days, points, today+"-"+user_id)
    pic_url = "https://www.d2robot.site/image/" + pic_name
    send = "<@%s>" % message.author.id
    await message.reply(content=send, pic_url=pic_url)
