# -*- coding: utf-8 -*-
from aiohttp import web, WSCloseCode
import aiohttp_jinja2
import jinja2


async def root(request):
    return web.Response(text="Please open /<username> page")


async def ws(request):
    ws = web.WebSocketResponse()
    request.app['websockets'].append(ws)
    await ws.prepare(request)
    return ws


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')

app = web.Application(debug=True)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static/', path='static', show_index=True)

app.router.add_route('*', '/', root)
app.router.add_route('*', '/{user}/ws', ws)

app['websockets'] = []
app.on_shutdown.append(on_shutdown)

web.run_app(app)
