#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: format

:Synopsis:

:Author:
    servilla

:Created:
    1/27/20
"""
import json

import daiquiri

from webapp.exceptions import FormatError

logger = daiquiri.getLogger(__name__)


class Formatter(object):
    def __init__(self, stylized: list):
        self._stylized = stylized

    def format(self, accept: str):
        if accept in formats:
            formatter = formats[accept]
            formatted = formatter(self._stylized)
            return formatted
        else:
            msg = f"Unrecognized format requested: {accept}"
            raise FormatError(msg)


def application_json(stylized: dict):
    return json.dumps(stylized)


def text_html(stylized: dict):
    if "doi" in stylized:
        doi = stylized["doi"]
        if doi[-1] == ".":
            doi = doi.strip(".")
            stylized["doi"] = f"<a href='{doi}'>{doi}</a>."
        else:
            stylized["doi"] = f"<a href='{doi}'>{doi}</a>"

    items = list()
    for item in stylized:
        items.append(stylized[item])
    return " ".join(items)



def text_plain(stylized: dict):
    items = list()
    for item in stylized:
        items.append(stylized[item])
    return " ".join(items)


formats = {
    "application/json": application_json,
    "text/html": text_html,
    "text/plain": text_plain }