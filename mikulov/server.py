# -*- coding: utf-8 -*-
from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging
import sys
import backend


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(name)-15s: %(filename)s:%(lineno)-3d: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger('frontend')


@aiohttp_jinja2.template('root.jinja2')
async def root(request):
    return {}


@aiohttp_jinja2.template('post.jinja2')
async def new_post(request):
    logger.info("new_post")
    data = await request.post()
    logger.info("data: %s", data)
    # TODO: Trap exceptions here
    token, url = await backend.make_a_post(data)
    return {
        "token": token,
        "url": url
    }


@aiohttp_jinja2.template('display.jinja2')
async def display_post(request):
    logger.info("display_post")
    digest = request.match_info['digest']
    slug = request.match_info['slug']
    title, contents = await backend.get_post(digest, slug)
    return {
        'title': title,
        'contents': contents
    }


app = web.Application(debug=True)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static/', path='static', show_index=True)

app.router.add_route('*', '/', root)
app.router.add_route('POST', '/post', new_post)
app.router.add_route('GET', '/{digest}-{slug}', display_post)

web.run_app(app)
