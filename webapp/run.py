#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: run

:Synopsis:
 
:Author:
    servilla

:Created:
    01/10/2020
"""
import daiquiri
from flask import abort, Flask, request, send_file
import requests

from webapp.config import Config

logger = daiquiri.getLogger('run.py: ' + __name__)

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/cite')
def hello_world():
    return 'Hello on Wheels!'


@app.route('/cite/<pid>')
def cite(pid=None):
    env = request.args.get('env')
    format = request.args.get('format')

    if pid is None:
        return 'Help!'
    try:
        #response = citation(pid=pid, env=env, format=format)
        pass
        return 'response'
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        abort(400)


if __name__ == '__main__':
    app.run()
