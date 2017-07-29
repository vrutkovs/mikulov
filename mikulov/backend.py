# -*- coding: utf-8 -*-
import logging
import sys


logger = logging.getLogger(__name__)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(name)-15s: %(filename)s:%(lineno)-3d: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger('backend')


async def make_a_post(data):
    logger.info("make_a_post")
    return (
        "wubbadubbadubdubs",
        "/1234-test-post"
    )
