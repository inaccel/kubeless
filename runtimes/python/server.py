import imp
import json
import multiprocessing
import os

from gunicorn.app.base import BaseApplication
from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import ServiceUnavailable

module = imp.load_source('function', '%s/%s.py' % (os.getenv('INACCEL_WORKDIR', '/inaccel'), os.getenv('MOD_NAME')))

function = getattr(module, os.getenv('FUNC_HANDLER'))

function_timeout = float(os.getenv('FUNC_TIMEOUT', 180))

memory_limit_in_mb = os.getenv('FUNC_MEMORY_LIMIT')

context = {
    'function_name': function,
    'function_version': function,
    'function_timeout': function_timeout,
    'memory_limit_in_mb': memory_limit_in_mb,
}

ready = multiprocessing.Event()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def handler():
    if ready.is_set():
        event = {
            'httpMethod': request.method,
            'path': request.path,
            'queryStringParameters': request.args.to_dict(),
            'protocol': request.environ.get('SERVER_PROTOCOL'),
            'headers': json.dumps({k:v for k, v in request.headers.items()}),
            'data': request.get_data(),
            'json': request.get_json(force=True, silent=True),
            'form': request.form.to_dict(),
        }
        return function(event, context)

    else:
        raise ServiceUnavailable

@app.route('/healthz', methods=['GET'])
def healthz():
    return 'OK'

def install_bitstreams():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('bitstream', nargs='*')
    args = parser.parse_args()

    for bitstream in args.bitstream:
        os.system('inaccel bitstream install {}'.format(bitstream))

    ready.set()

def number_of_threads():
    return 2 * multiprocessing.cpu_count() + 1

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(install_bitstreams)

    options = {
        'accesslog': '-',
        'bind': '%s:%s' % ('0.0.0.0', os.environ.get('FUNC_PORT', os.environ.get('PORT', 8080))),
        'workers': 1,
        'threads': number_of_threads(),
    }
