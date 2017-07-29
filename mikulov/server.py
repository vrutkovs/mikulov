# -*- coding: utf-8 -*-
from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging
import sys


logger = logging.getLogger(__name__)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(name)-25s: %(filename)s:%(lineno)-3d: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger('mikulov')


@aiohttp_jinja2.template('root.jinja2')
async def root(request):
    return {}


@aiohttp_jinja2.template('post.jinja2')
async def new_post(request):
    logger.info("new_post")
    return {}

app = web.Application(debug=True)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static/', path='static', show_index=True)

app.router.add_route('*', '/', root)
app.router.add_route('POST', '/post', new_post)

web.run_app(app)
