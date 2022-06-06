import os
import datetime

from . import database
from . import cache

db: database.RobotData = None
rds: cache.RobotCache = None


def init_dao():
    global db, rds

    db_host = os.environ['ROBOT_DB_HOST']
    db = database.RobotData(db_host, 3306, 'develop', 'Sjzez=19480913', 'robot', 600)

    rds = cache.RobotCache()


def check_is_signed(user_id):
    sql = "select count(1) from `user_sign_log` where true and "
    time_today = datetime.date.today()
    condition = "`user_id`='%s' and date_format(`sign_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_today)
    cnt = db.do_select_cnt(sql + condition)
    return cnt


def get_continuous_days(user_id):
    sql = "select `days` from `user_continuous_sign` where true and "
    time_today = datetime.date.today()
    condition = "`user_id`='%s' and date_format(`update_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_today)
    lines = db.do_select(sql + condition)
    if len(lines) == 0:
        days = 0
    else:
        days = lines[0][0]
    return days


def check_is_continuous(user_id):
    sql = "select `id` from `user_continuous_sign` where true and "
    time_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    condition = "`user_id`='%s' and date_format(`update_time`,'%%Y-%%m-%%d')=date_format('%s','%%Y-%%m-%%d')" % (user_id, time_yesterday)
    lines = db.do_select(sql + condition)
    if len(lines) == 0:
        auto_id = 0
    else:
        auto_id = lines[0][0]
    return auto_id


def insert_continuous_beginning(user_id):
    sql = "insert into `user_continuous_sign`(`user_id`, `days`) values(%s,%s)"
    val = (user_id, 1)
    db.do_insert(sql, val)
    return 0


def update_continuous_days(id):
    sql = "update `user_continuous_sign` set `days`=`days`+1 where `id`=%s"
    val = (id)
    db.do_update(sql, val)
    return 0


def user_sign(user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel):
    if sign_time == "":
        sign_time_fmt = datetime.datetime.now()
    else:
        sign_time_fmt = datetime.datetime.strptime(sign_time+" 12:00:00", "%Y-%m-%d %H:%M:%S")
    _do_insert_sign_data(user_id, sign_reward, sign_type, sign_time_fmt, sign_guild, sign_channel)


def _do_insert_sign_data(user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel):
    sql = "insert into `user_sign_log`(`user_id`, `sign_reward`, `sign_type`, `sign_time`, `sign_guild`, `sign_channel`) values(%s,%s,%s,%s,%s,%s)"
    val = (user_id, sign_reward, sign_type, sign_time, sign_guild, sign_channel)
    db.do_insert(sql, val)


def get_sign_info(user_id):
    sql = "select count(1)c0, count(distinct date_format(`sign_time`,'%Y-%m-%d'))c1 from `user_sign_log` where true and "
    condition = "`user_id`='%s'" % user_id
    ret_data = db.do_select(sql + condition)[0]
    cnt_all = ret_data[0]
    cnt_day = ret_data[1]
    points = _get_user_points(user_id)
    return cnt_all, cnt_day, points


def _get_user_points(user_id):
    sql = "select `days` from `user_continuous_sign` where `user_id`=%s" % user_id
    data_lines = db.do_select(sql)

    day_points = 0
    con_points = 0
    for line in data_lines:
        line_day = int(line[0])
        day_points += line_day
        con_points += _calculate_points_by_days(line_day)
    return day_points + con_points


def _calculate_points_by_days(days):
    _cal_period = 30
    _points_mon = 19
    p_mon = int(days / _cal_period) * _points_mon
    d_res = days % _cal_period
    if d_res >= 15:
        p_res = 5
    elif d_res >= 7:
        p_res = 3
    elif d_res >= 3:
        p_res = 1
    else:
        p_res = 0

    return p_mon + p_res
