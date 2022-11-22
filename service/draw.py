import dao
from botpy.message import Message

import hashlib
import datetime

_daily_control = "_draw_one_destiny"
_default_slat = "ZZLX_KJJY_GHGY_LJRW"
_suffix = "_draw_one"


async def service_draw_get_one(message: Message):
    uid = message.author.id
    uid_date = _get_uid_date(uid)

    content_arr = message.content.split()
    if len(content_arr) >= 3:
        if content_arr[2] == "逆天改命":
            if len(content_arr) == 3:
                await message.reply(content="<@%s> 别忘了咒语: /抽签 逆天改命 [任意咒语(不能空着)]" % uid)
            else:
                words = content_arr[3]
                await service_draw_change_destiny(message, words)
        else:
            await message.reply(content="<@%s> 请摆正姿势: /抽签 逆天改命 [任意咒语(不能空着)]" % uid)
    else:
        num = _get_num_from_cache(uid_date)
        if num is None:
            num = _draw_inner_get_unique_id_by_day(uid_date)
            _set_num_to_cache(uid_date, num)

        draw_poem = dao.get_draw_one_poem(num)
        send = "<@%s> 久等啦！您抽中的是第 %d 签\n签诗：%s\n" % (uid, num, draw_poem)
        await message.reply(content=send)


async def service_draw_solve_one(message: Message):
    uid = message.author.id
    uid_date = _get_uid_date(uid)
    num = _get_num_from_cache(uid_date)
    if num is None:
        send = "<@%s> 你还没有抽签\n" % uid
    else:
        draw_explain = dao.get_draw_one_explain(num)
        send = "<@%s> 解签：%s\n" % (uid, draw_explain)
    await message.reply(content=send)


async def service_draw_change_destiny(message: Message, words):
    uid = message.author.id
    uid_date = _get_uid_date(uid)
    destiny_key = uid_date + "_" + _daily_control
    is_words_set = dao.get_draw_one_destiny_words(destiny_key)
    if is_words_set is None:
        dao.set_draw_one_destiny_words(destiny_key, words)
        _del_num_from_cache(uid_date)
        send = "<@%s> 少年可以继续抽签了" % uid
    else:
        send = "<@%s> 请明日再来" % uid
    await message.reply(content=send)


def _get_uid_date(user_id):
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    return user_id + "_" + today_str


def _get_num_from_cache(uid_date):
    cache_key = uid_date + _suffix
    return dao.get_draw_one_number(cache_key)


def _del_num_from_cache(uid_date):
    cache_key = uid_date + _suffix
    return dao.del_draw_one_number(cache_key)


def _set_num_to_cache(uid_date, num):
    cache_key = uid_date + _suffix
    return dao.set_draw_one_number(cache_key, num)


def _draw_inner_get_unique_id_by_day(uid_date):
    file_len = dao.get_draw_one_len()
    destiny_key = uid_date + "_" + _daily_control
    words_set = dao.get_draw_one_destiny_words(destiny_key)
    if words_set is None:
        unique_key = uid_date + "_" + _default_slat
    else:
        unique_key = uid_date + "_" + words_set
    key_md5 = hashlib.md5(unique_key.encode('utf-8'))
    key_int = int(key_md5.hexdigest(), 16)
    num = key_int % file_len + 1
    return num
