import os
import datetime

from . import database
from . import cache
from . import file

db: database.RobotData = None
rds: cache.RobotCache = None
fl: file.RobotFile = None
managers_list: list[str] = None


def init_dao():
    global db, rds, fl, managers_list

    db_host = os.environ['POME_DB_HOST']
    db_port = os.environ['POME_DB_PORT']
    db_user = os.environ['POME_DB_USER']
    db_pwd = os.environ['POME_DB_PWD']
    db_database = os.environ['POME_DB_DATABASE']

    db = database.RobotData(db_host, int(db_port), db_user, db_pwd, db_database, 600)

    rds = cache.RobotCache()

    managers_list = os.environ['MANAGERS_LIST'].split(",")

    draw_one_dir = os.environ['DRAW_ONE_FILE']
    fl = file.RobotFile(draw_one_dir)


def get_managers_list():
    return managers_list


def redis_activity_status_set(status):
    if status == "start":
        rds.set_data("activity_first", "1")
    else:
        rds.set_data("activity_first", "0")


def redis_activity_status_get():
    return rds.get_data("activity_first")


def redis_activity_participate(uid):
    rds.sadd_data("activity_names", uid)
    return 0


def redis_activity_get_result():
    res = rds.lrange_data("activity_result_list")
    if res is None:
        return redis_activity_generate_res()
    else:
        return res


def redis_activity_generate_res():
    return []


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
    points, details = _get_user_points(user_id)
    return cnt_all, cnt_day, points, details


def _get_user_points(user_id):
    sql = "select `days` from `user_continuous_sign` where `user_id`=%s" % user_id
    data_lines = db.do_select(sql)

    day_points = 0
    con_points = 0
    con_details = [0, 0, 0, 0]

    for line in data_lines:
        line_day = int(line[0])
        day_points += line_day
        calculate_res = _calculate_points_by_days(line_day)
        con_points += calculate_res[0]
        for i in range(4):
            con_details[i] += calculate_res[i+1]

    return [day_points + con_points, con_details]


def _calculate_points_by_days(days):
    _cal_period = 30
    _points_30 = 10
    _points_15 = 5
    _points_07 = 3
    _points_03 = 1

    d_30 = int(days / _cal_period)
    p_mon = d_30 * (_points_30 + _points_15 + _points_07 + _points_03)

    d_res = days % _cal_period
    if d_res >= 15:
        d_15 = 1
    else:
        d_15 = 0
    if d_res >= 7:
        d_07 = 1
    else:
        d_07 = 0
    if d_res >= 3:
        d_03 = 1
    else:
        d_03 = 0
    p_res = d_15 * _points_15 + d_07 * _points_07 + d_03 * _points_03

    return [p_mon + p_res, d_30, d_15+d_30, d_07+d_30, d_03+d_30]


def get_draw_one_number(key):
    res = rds.get_data(key)
    if res is not None:
        res = int(res)
    return res


def del_draw_one_number(key):
    rds.rm_data(key)
    return 0


def set_draw_one_number(key, val):
    rds.set_data_exp(key, val, 86400)
    return 0


def get_draw_one_len():
    return fl.draw_one_len


def get_draw_one_poem(num):
    return fl.draw_one_map[num][0]


def get_draw_one_explain(num):
    return fl.draw_one_map[num][1]


def get_draw_one_destiny_words(key):
    res = rds.get_data(key)
    if res is not None:
        res = str(res)
    else:
        res = None
    return res


def set_draw_one_destiny_words(key, val):
    rds.set_data_exp(key, val, 86400)
    return 0
