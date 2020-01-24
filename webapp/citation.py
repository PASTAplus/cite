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
import json
import os

import daiquiri
from lxml import etree
import requests

from webapp import utils
from webapp.config import Config
from webapp.eml import Eml
from webapp.eml import Creator

logger = daiquiri.getLogger(__name__)


def authors(creators: list) -> list:
    a = list()
    for creator in creators:
        c = dict()
        individual_names = creator.individualNames
        i = list()
        for individual_name in individual_names:
            name = dict()
            name["surname"] = individual_name.surName
            name["given_names"] = individual_name.givenNames
            i.append(name)
        c["individual_names"] = i
        c["organization_names"] = creator.organizationNames
        c["position_names"] = creator.positionNames
        a.append(c)
    return a


def citation_json(title: str, pubdate: str, creators: Creator, doi: str) -> dict:
    j = dict()
    j["title"] = title
    j["pubdate"] = pubdate
    j["doi"] = doi
    j["authors"] = authors(creators=creators)
    j["publisher"] = "Environmental Data Initiative"
    return j


def organizations(creators: list) -> list:
    o = list()
    for creator in creators:
        if len(creator.individualNames) == 0 and \
           len(creator.positionNames) == 0 and \
           len(creator.organizationNames) > 0:
            organization_names = creator.organizationNames
            for organization_name in organization_names:
                o.append(organization_name)
    return o


def resource_metadata(rmd: str):
    upload_date = None
    doi = None
    _ = etree.fromstring(rmd.encode('utf-8'))
    date_created = _.find('.//dateCreated').text
    upload_date = date_created.split(' ')[0]
    doi = _.find('.//doi').text
    return upload_date, doi


def pub_year(pubdate: str) -> str:
    year = pubdate.split("-")[0]
    return year


class Citation(object):
    def __init__(self, pid: str, env: str, accept: str):
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
                self._j = json.load(fp)
        else:
            scope, identifier, revision = utils.pid_triple(pid)
            eml_uri = f"{pasta}/metadata/eml/{scope}/{identifier}/{revision}"
            rmd_uri = f"{pasta}/rmd/eml/{scope}/{identifier}/{revision}"

            r = requests.get(eml_uri)
            if r.status_code == requests.codes.ok:
                eml = Eml(eml=r.text)
            else:
                raise requests.exceptions.ConnectionError()

            r = requests.get(rmd_uri)
            if r.status_code == requests.codes.ok:
                pubdate, doi = resource_metadata(rmd=r.text)
            else:
                raise requests.exceptions.ConnectionError()

            self._j = citation_json(title=eml.title, pubdate=pubdate,
                                    creators=eml.creators, doi=doi)
            with open(file_path, "w") as fp:
                json.dump(self._j, fp)

        self._citation = str(self._j)

    @property
    def citation(self):
        return self._citation

