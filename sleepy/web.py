

from threading import Thread
from sleepy import config
import bottle as b


@b.route('/')
def index():
    return 'sleepy config backend'


class WebBackendThread(Thread):

    def run(self):
        # server = config.get().get('default', 'server', fallback='')
        port = config.get().getint('default', 'port', fallback=8080)
        b.run(port=port, debug=True)

