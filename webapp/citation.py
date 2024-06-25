#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: citation

:Synopsis:
    Generates a PASTA data package citation using the requested style and
    in the accepted mime-type.

:Author:
    servilla

:Created:
    1/21/20
"""
from datetime import datetime
import json
import os
from urllib.parse import urlparse

import daiquiri

from webapp.config import Config
from webapp.eml import Eml
from webapp.exceptions import DataPackageError
from webapp.exceptions import PastaEnvironmentError
from webapp.format import Formatter
from webapp.style import Stylizer
from webapp.utils import requests_wrapper
from webapp.utils import resource_metadata

logger = daiquiri.getLogger(__name__)


class Citation(object):
    def __init__(
        self,
        pid: str,
        env: str,
        style: str,
        accept: str,
        access: bool,
        ignores: list,
        no_dot: bool,
    ):

        eml_url = None
        rmd_url = None

        if env.lower() in ("d", "dev", "development"):
            pasta = Config.PASTA_D
            cache = Config.CACHE_D
            env = Config.ENV_D
        elif env.lower() in ("s", "stage", "staging"):
            pasta = Config.PASTA_S
            cache = Config.CACHE_S
            env = Config.ENV_S
        elif env.lower() in ("p", "prod", "production"):
            pasta = Config.PASTA_P
            cache = Config.CACHE_P
            env = Config.ENV_P
        elif _is_valid_url(env):
            eml_url = env
            pasta = None
            cache = None
        else:
            msg = f"Requested PASTA environment not supported: {env}"
            raise PastaEnvironmentError(msg)

        if eml_url is None:
            file_path = f"{cache}{pid}.json"

            if os.path.isfile(file_path):
                # Read from cached location
                with open(file_path, "r") as fp:
                    self._citation = json.load(fp)
            else:
                scope, identifier, revision = pid.strip().split(".")
                eml_url = f"{pasta}/metadata/eml/{scope}/{identifier}/{revision}"
                rmd_url = f"{pasta}/rmd/eml/{scope}/{identifier}/{revision}"

        try:
            if eml_url is not None:
                eml = Eml(requests_wrapper(eml_url))
            if rmd_url is not None:
                pubdate, doi = resource_metadata(requests_wrapper(rmd_url))
            else:
                pubdate = datetime.now().year
                doi = "doi:DOI_PLACE_HOLDER"
        except ValueError as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.error(e)
            msg = (
                f'Error accessing data package "{pid}" in the "'
                f'{env}" environment'
            )
            raise DataPackageError(msg)

        # Obsfucate test DOIs
        if env != Config.ENV_P:
            doi = "doi:DOI_PLACE_HOLDER"

        self._citation = _make_base_citation(
            eml.title, pubdate, revision, doi, eml.creators
        )
        with open(file_path, "w") as fp:
            json.dump(self._citation, fp)

        if len(ignores) > 0:
            authors = _ignore(ignores, self._citation["authors"])
            if len(authors) == 0:
                msg = "Author list is empty"
                raise ValueError(msg)
            else:
                self._citation["authors"] = authors

        self._stylizer = Stylizer(self._citation)
        self._stylized = self._stylizer.stylize(style, pid, access, no_dot)
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


def _make_base_citation(
    title: str, pubdate: str, version: str, doi: str, authors: list
) -> dict:
    citation = dict()
    citation["title"] = title
    citation["pubdate"] = pubdate
    citation["version"] = version
    citation["doi"] = doi
    citation["authors"] = authors
    citation["publisher"] = Config.PUBLISHER
    return citation


def _ignore(ignores: list, authors: list) -> list:
    _authors = list()
    for author in authors:
        if "INDIVIDUALS" in ignores:
            author["individual_names"] = []
        if "ORGANIZATIONS" in ignores:
            author["organization_names"] = []
        if "POSITIONS" in ignores:
            author["position_names"] = []
        if not _is_empty_author(author):
            _authors.append(author)
    return _authors


def _is_empty_author(author: dict) -> bool:
    if (
        len(author["individual_names"]) == 0
        and len(author["organization_names"]) == 0
        and len(author["position_names"]) == 0
    ):
        return True
    else:
        return False


def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
