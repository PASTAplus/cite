#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: citation

:Synopsis:

:Author:
    servilla

:Created:
    1/21/20
"""
import copy
import json
import os

import daiquiri

from webapp.config import Config
from webapp.eml import Eml
from webapp.format import Formatter
from webapp.style import Stylizer
from webapp.utils import requests_wrapper
from webapp.utils import resource_metadata

logger = daiquiri.getLogger(__name__)


class Citation(object):

    def __init__(self, pid: str, env: str, style: str, accept: str):

        if env in ('d', 'dev', 'development'):
            pasta = Config.PASTA_D
            cache = Config.CACHE_D
        elif env in ('s', 'stage', 'staging'):
            pasta = Config.PASTA_S
            cache = Config.CACHE_S
        else:
            pasta = Config.PASTA_P
            cache = Config.CACHE_P

        file_path = f'{cache}{pid}.json'

        if os.path.isfile(file_path):
            # Read from cached location
            with open(file_path, "r") as fp:
                self._citation = json.load(fp)

        else:
            scope, identifier, revision = pid.strip().split(".")
            eml_url = f"{pasta}/metadata/eml/{scope}/{identifier}/{revision}"
            rmd_url = f"{pasta}/rmd/eml/{scope}/{identifier}/{revision}"

            eml = Eml(requests_wrapper(eml_url))
            pubdate, doi = resource_metadata(requests_wrapper(rmd_url))

            self._citation = _make_base_citation(eml.title, pubdate, revision,
                                                 doi, eml.creators)
            with open(file_path, "w") as fp:
                json.dump(self._citation, fp)

        self._stylizer = Stylizer(self._citation)
        self._stylized = self._stylizer.stylize(style)
        self._formatter = Formatter(self._stylized)
        self._media_type, self._formatted = self._formatter.format(accept)


    @property
    def base(self):
        return self._citation

    @property
    def formatted(self):
        return self._formatted

    @property
    def media(self):
        return self._media_type

    @property
    def stylized(self):
        return self._stylized


def _make_base_citation(title: str, pubdate: str, version: str,
                        doi: str, authors: list) -> dict:
    citation = dict()
    citation["title"] = title
    citation["pubdate"] = pubdate
    citation["version"] = version
    citation["doi"] = doi
    citation["authors"] = authors
    citation["publisher"] = Config.PUBLISHER
    return citation
