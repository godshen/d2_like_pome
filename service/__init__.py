from .always import init_service

from .sign import (
    service_user_do_sign,
    service_user_re_sign,
    service_get_sign_info
)

from .default import (
    service_default,
    service_word_config
)

from .weather import service_get_city_weather

from .manage import (
    service_manage,
    service_manage_err
)
