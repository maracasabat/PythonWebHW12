from aiohttp import web
import jinja2
import aiohttp_jinja2


def setup_routes(application):
    from src.routes import setup_routes as setup_routes_src
    setup_routes_src(application)


def setup_libs(application: web.Application):
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader('templates'))


def create_app(application):
    setup_libs(application)
    setup_routes(application)


app = web.Application()


if __name__ == '__main__':
    create_app(app)
    web.run_app(app)
