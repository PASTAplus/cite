#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: run

:Synopsis:
 
:Author:
    servilla

:Created:
    01/10/2020
"""
import logging
import os

import daiquiri
from flask import abort, Flask, make_response, request, send_file

from webapp.citation import Citation
from webapp.config import Config

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/run.log"
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile),
                                            "stderr"))
logger = daiquiri.getLogger("run.py: " + __name__)


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/cite")
@app.route("/cite/help")
def help():
    return "help!"


@app.route("/cite/<pid>")
def cite(pid=None):
    env = request.args.get("env")
    if env is None: env = Config.DEFAULT_ENV
    style = request.args.get("style")
    if style is None: style = Config.DEFAULT_STYLE
    accept = request.headers.get("Accept")
    if accept is None or accept == "*/*": accept = Config.DEFAULT_ACCEPT
    accept = accept.split(",")[0]
    # TODO token = request.args.get("token")

    try:
        citation = Citation(pid, env, style, accept)
        response = make_response(citation.formatted)
        response.headers['Content-Type'] = accept
        return response
    except Exception as e:
        logger.error(e)
        abort(400)


if __name__ == "__main__":
    app.run()
