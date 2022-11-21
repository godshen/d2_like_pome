from .always import init_service

from .sign import (
    service_user_do_sign,
    service_user_re_sign,
    service_get_sign_info,
    service_get_sign_picture,
)

from .default import (
    service_default,
    service_word_config,
)

from .weather import service_get_city_weather

from .manage import (
    service_manage,
    service_manage_err,
    managers,
)

from .activity import (
    activity_at_start,
    activity_at_end,
    activity_at_join,
    activity_get_result,
)

from .draw import (
    service_draw_get_one,
    service_draw_solve_one,
)
