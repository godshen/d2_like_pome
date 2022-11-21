# !/usr/bin/python
# -*- coding: UTF-8 -*-
import server
from botpy import logging


if __name__ == "__main__":
    print("sjzez great forever")

    client, appid, token = server.init_project()
    server.run_project(client, appid, token)

    logger = logging.get_logger()
    logger.info("Init Project SUCCESS")
