# -*- coding: utf-8 -*-
from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging


logger = logging.getLogger(__name__)


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
