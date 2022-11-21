import dao
from botpy.message import Message

import hashlib
import datetime

_slat = "ZZLX_KJJY_GHGY_LJRW"
_suffix = "_draw_one"


async def service_draw_get_one(message: Message):
    uid = message.author.id
    uid_date = _get_uid_date(uid)
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


def _get_uid_date(user_id):
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    return user_id + "_" + today_str


def _get_num_from_cache(uid_date):
    cache_key = uid_date + _suffix
    return dao.get_draw_one_number(cache_key)


def _set_num_to_cache(uid_date, num):
    cache_key = uid_date + _suffix
    return dao.set_draw_one_number(cache_key, num)


def _draw_inner_get_unique_id_by_day(uid_date):
    file_len = dao.get_draw_one_len()
    unique_key = uid_date + "_" + _slat
    key_md5 = hashlib.md5(unique_key.encode('utf-8'))
    key_int = int(key_md5.hexdigest(), 16)
    num = key_int % file_len + 1
    return num
