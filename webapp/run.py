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
from flask import abort, Flask, request, send_file

from webapp.citation import Citation
from webapp.config import Config
from webapp.eml import Eml

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
    accept = request.headers.get("Accept")
    # TODO token = request.args.get("token")

    try:
        citation = Citation(pid=pid, env=env, accept=accept)
        response = citation.citation
        return response
    except Exception as e:
        logger.error(e)
        abort(400)


if __name__ == "__main__":
    app.run()
