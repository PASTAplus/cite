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
from webapp.eml import Eml

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
    accept = request.args.get("format")
    # TODO token = request.args.get("token")
    try:
        response = citation(pid=pid, env=env, accept=accept)
        return response
    except Exception as e:
        logger.error(e)
        abort(400)


def citation(pid: str = None, env: str = "p", accept: str = "text/html") -> str:
    c = None
    scope, identifier, revision = pid_triple(pid)
    url = f"{Config.PASTA_P}/metadata/eml/{scope}/{identifier}/{revision}"
    r = requests.get(url)
    eml = Eml(r.text)
    c = f"Your package identifier is {pid}!"
    return c


def pid_triple(pid: str) -> tuple:
    _ = pid.strip().split(".")
    scope = str(_[0])
    identifier = int(_[1])
    revision = int(_[2])
    return scope, identifier, revision


if __name__ == "__main__":
    app.run()
