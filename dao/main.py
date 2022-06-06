# !/usr/bin/python
# -*- coding: UTF-8 -*-

from business import init_dao

sql_list = [
    "desc `user_sign_log`",
    "select count(1) cnt from `user_sign_log`",
    "select * from `user_sign_log`",
    "select count(1) cnt from `user_continuous_sign`",
    "select * from `user_continuous_sign`",
]

if __name__ == "__main__":
    init_dao()
