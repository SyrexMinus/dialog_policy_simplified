from aiohttp import web


async def handle(request):
    kafka_request = request.match_info.get('kafka_request', "Anonymous")
    text = f"I have got following kafka request: {kafka_request}"
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{kafka_request}', handle)])

if __name__ == '__main__':
    web.run_app(app)
