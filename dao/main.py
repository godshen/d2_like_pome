# !/usr/bin/python
# -*- coding: UTF-8 -*-

from db import RobotData

sql_list = [
    "desc user_sign_log",
    "select count(1)cnt from user_sign_log",
    "select * from user_sign_log",
    # "alter table `user_sign_log` add column `sign_channel` varchar(100) not null default '' comment '子频道名称' after `sign_guild`",
    # "alter table `user_sign_log` add column `sign_channel` varchar(100) not null default '' comment '子频道名称' after `sign_guild`",
    "insert into `user_sign_log`(`user_id`, `sign_reward`, `sign_type`, `sign_guild`, `sign_channel`) values(%s,%s,%s,%s,%s)",
    "select `user_id`, `sign_reward`, `sign_type`, date_format(`sign_time`,'%Y-%m-%d') `sign_t` from user_sign_log",
    "select count(1)c0, count(distinct date_format(`sign_time`,'%Y-%m-%d'))c1 from `user_sign_log` where true and ",
]

if __name__ == "__main__":
    print("demo of mysql")
    # 打开数据库连接
    db = RobotData(
        '34.92.55.1', 3306, 'develop',
        'Sjzez=19480913', 'robot', 600
    )
    # print(db.get_version())
    # db.do_insert(sql_list[3], ("shenzh0713", "积分", 1, "10000", "10000100001"))
    data_lines = db.do_select(sql_list[4])
    print("data len of return is %d" % len(data_lines))
    for line in data_lines:
        print("\t", end="")
        print(line)

    condition = "`user_id`='%s'" % '5825676483738802511'
    print(db.do_select(sql_list[5] + condition))

    db.close()

