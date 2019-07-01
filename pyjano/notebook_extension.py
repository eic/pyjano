import tornado.web
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler


class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('Hello, world!')


class CorsStaticFileHandler(tornado.web.StaticFileHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

def load_jupyter_server_extension(nb_app):
    '''
    Register a hello world handler.

    Based on https://github.com/Carreau/jupyter-book/blob/master/extensions/server_ext.py
    '''
    from pprint import pprint

    web_app = nb_app.web_app

    nb_app.log.debug("=" * 30)
    nb_app.log.debug('Setting Pyjano nb server extension')
    nb_app.log.debug(type(web_app))
    # pprint(vars(nb_app))
    # pprint(vars(web_app))
    nb_app.log.debug("=" * 30)

    host_pattern = '.*$'
    #route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
    #web_app.add_handlers(host_pattern, [(route_pattern, tornado.web.StaticFileHandler)])
    web_app.add_handlers(host_pattern, [(r"/rjs/(.*)", CorsStaticFileHandler, {"path": web_app.settings['server_root_dir'], "default_filename": "root_browser.html"})])
    #web_app.add_handlers(host_pattern, [(route_pattern, tornado.web.StaticFileHandler, {"path":r"/home/romanov/ceic/static"})])