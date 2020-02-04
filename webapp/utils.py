#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: utils

:Synopsis:

:Author:
    servilla

:Created:
    1/23/20
"""
import daiquiri
import requests
from lxml import etree

logger = daiquiri.getLogger(__name__)


def doi_url(doi: str) -> str:
    url = "https://doi.org/"
    return doi.replace("doi:", url)


def initials(names: list, dot: bool = True) -> str:
    if dot:
        return "".join(map(lambda s: f"{s[0]}.", names))
    else:
        return "".join(map(lambda s: f"{s[0]}", names))


def pub_year(pubdate: str) -> str:
    year = pubdate.split("-")[0]
    return year


def requests_wrapper(url: str) -> str:
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise requests.exceptions.ConnectionError()


def resource_metadata(rmd: str):
    _ = etree.fromstring(rmd.encode('utf-8'))
    date_created = _.find('.//dateCreated').text
    upload_date = date_created.split(' ')[0]
    doi = _.find('.//doi').text
    return upload_date, doi
