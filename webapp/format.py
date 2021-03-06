#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: format

:Synopsis:
    Formats a PASTA data package citation into the accepted mime-type.

:Author:
    servilla

:Created:
    1/27/20
"""
import json

import daiquiri

from webapp.config import Config
from webapp.exceptions import FormatError

logger = daiquiri.getLogger(__name__)


class Formatter(object):
    def __init__(self, stylized: dict):
        self._stylized = stylized

    def format(self, accept: str):
        accepts = [_.strip() for _ in accept.split(",")]
        for media_type in accepts:
            if media_type in ("*/*", "text/*"):
                media_type = Config.DEFAULT_ACCEPT
            if media_type in formats:
                formatter = formats[media_type]
                formatted = formatter(self._stylized)
                return media_type, formatted
        msg = f"Accepted format(s) not supported: {accept}"
        raise FormatError(msg)


def application_json(stylized: dict):
    if "citation" in stylized:
        stylized = stylized["citation"]
    return json.dumps(stylized, indent=2)


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
        items.append(str(stylized[item]))
    return " ".join(items)


def text_plain(stylized: dict):
    items = list()
    for item in stylized:
        items.append(str(stylized[item]))
    return " ".join(items)


formats = {
    "application/json": application_json,
    "text/html": text_html,
    "text/plain": text_plain
}
