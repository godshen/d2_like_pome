# -*- coding: utf-8 -*-

from .database import RobotData
from .business import (
    init_dao,
    check_is_signed,
    get_continuous_days,
    check_is_continuous,
    insert_continuous_beginning,
    update_continuous_days,
    user_sign,
    get_sign_info,
    redis_activity_status_set,
    redis_activity_status_get,
    redis_activity_participate,
    redis_activity_get_result,
    get_managers_list,
    get_draw_one_number,
    set_draw_one_number,
    get_draw_one_poem,
    get_draw_one_explain,
    get_draw_one_len,
    get_draw_one_destiny_words,
    set_draw_one_destiny_words,
)
