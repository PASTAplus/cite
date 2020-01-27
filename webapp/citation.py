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
import pendulum

from webapp.config import Config
from webapp.eml import Eml
from webapp.exceptions import StyleError
from webapp.style import Stylizer
from webapp.utils import doi_url
from webapp.utils import initials
from webapp.utils import pub_year
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

        self._stylizer = Stylizer(style)
        self._stylized = self._stylizer.stylize(self._citation, accept)

    @property
    def base(self):
        return self._citation

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

#
#
# def _stylizer(citation: dict, style: str, accept: str) -> str:
#
#     stylized = list()
#
#     individuals = list()
#     authors = citation["authors"]
#     for author in authors:
#         individual_names = author["individual_names"]
#         for individual_name in individual_names:
#             given_names = individual_name["given_names"]
#             given_name_initials = initials(given_names)
#             sur_name = individual_name["sur_name"]
#             name = f"{given_name_initials} {sur_name}"
#             individuals.append(name.strip())
#
#     organizations = list()
#     authors = citation["authors"]
#     for author in authors:
#         individual_names = author["individual_names"]
#         position_names = author["position_names"]
#         organization_names = author["organization_names"]
#         if len(individual_names) == 0:
#             for organization_name in organization_names:
#                 organizations.append(organization_name)
#
#     positions = list()
#     authors = citation["authors"]
#     for author in authors:
#         individual_names = author["individual_names"]
#         position_names = author["position_names"]
#         organization_names = author["organization_names"]
#         if len(individual_names) == 0 and len(organization_names) == 0:
#             for position_name in position_names:
#                 positions.append(position_name)
#
#     # Reverse lead author name
#     if len(individuals) > 0:
#         lead_individual = individuals[0]
#         name = lead_individual.split(" ")
#         if len(name) == 2:
#             individuals[0] = f"{name[1]}, {name[0]}"
#
#     authors = individuals + organizations
#     if len(authors) > 0:
#         if len(authors) > 1:
#             authors[-1] = f"and {authors[-1]}"
#         if len(authors) == 2:
#             stylized.append(" ".join(authors))
#         elif len(authors) > 2:
#             stylized.append(", ".join(authors))
#         else:
#             author = authors[0].rstrip(".")
#             stylized.append(author)
#     else:
#         authors = positions
#         if len(authors) > 1:
#             authors[-1] = f"and {authors[-1]}"
#         if len(authors) == 2:
#             stylized.append(" ".join(authors))
#         elif len(authors) > 2:
#             stylized.append(", ".join(authors))
#         else:
#             author = authors[0].rstrip(".")
#             stylized.append(author)
#
#     stylized.append(". ")
#     stylized.append(pub_year(citation["pubdate"]))
#     stylized.append(". ")
#     stylized.append(citation["title"])
#     stylized.append(". ")
#     stylized.append("Version ")
#     stylized.append(citation["version"])
#     stylized.append(". ")
#     stylized.append(citation["publisher"])
#     stylized.append(". ")
#     doi = doi_url(citation["doi"])
#     if "text/html" in accept:
#         stylized.append(f"<a href='{doi}'>")
#         stylized.append(doi)
#         stylized.append("</a>")
#     else:
#         stylized.append(doi)
#     stylized.append(". ")
#
#     now = (pendulum.now("UTC")).format("D MMM YYYY", formatter="alternative")
#     stylized.append("Accessed ")
#     stylized.append(now)
#     stylized.append(". ")
#
#     return "".join(stylized)
