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
import json

import daiquiri
from flask import abort, Flask, request, send_file
import requests

from webapp.config import Config
from webapp.eml import Eml

open_tag = '<script type="application/ld+json">\n'
close_tag = "\n</script>"


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/run.log"
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile), "stdout"))
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
    title = None
    scope, identifier, revision = pid_triple(pid)
    url = f"{Config.PASTA_P}/metadata/eml/{scope}/{identifier}/{revision}"
    r = requests.get(url)
    eml = r.text
    eml = Eml(eml=eml)

    json_ld = dict()
    json_ld["@context"] = "http://cite.edirepository.org"
    json_ld["@type"] = "Citation"

    # if eml.creators is not None:
    #     creators = list()
    #     for creator in eml.creators:
    #         creators.append({'@type': 'Person', 'familyName': creator})
    #     json_ld['authors'] = creators
    json_ld["authors"] = "Authors"

    json_ld["title"] = eml.title
    json_ld["pubdate"] = eml.pubdate
    json_ld["publisher"] = "Environmental Data Initiative"
    json_ld["doi"] = "DOI Placeholder"

    j = json.dumps(json_ld, indent=2)

    response = f"{open_tag}{j}{close_tag}"

    return response

    # c = f"{pid} citation is {eml.creators}. {eml.pubdate}. {eml.title}. Environmental Data Initiative. DOI Placeholder"
    # return c


def pid_triple(pid: str) -> tuple:
    _ = pid.strip().split(".")
    scope = str(_[0])
    identifier = int(_[1])
    revision = int(_[2])
    return scope, identifier, revision


if __name__ == "__main__":
    app.run()
