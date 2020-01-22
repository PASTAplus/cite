#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: eml

:Synopsis:

:Author:
    servilla

:Created:
    01/11/2020
"""
from collections import namedtuple

import daiquiri
from lxml import etree

logger = daiquiri.getLogger("eml_2_1_1: " + __name__)


def flatten(element):
    t = ""
    if hasattr(element, "text"):
        t += element.text
    if hasattr(element, "__iter__"):
        for e in element:
            t += flatten(e)
    return t


def clean(text):
    return " ".join(text.split())


Creator = namedtuple('Creator', ['individualName', 'organizationName',
                                 'positionName'])
Creator.__new__.__defaults__ = (None, None, None)

IndividualName = namedtuple('IndividualName', ['givenName', 'surName'])
IndividualName.__new__.__defaults__ = (None, None)


class Eml(object):
    def __init__(self, eml: str):
        self._eml = eml.encode("utf-8")
        self._root = etree.fromstring(self._eml)
        self._title = self._get_title()
        self._pubdate = self._get_pubdate()
        self._creators = self._get_creators()
        pass

    def _get_creators(self):
        c = list()
        creators = self._root.findall(".//dataset/creator")
        for creator in creators:
            individual_names = list()
            individualNames = creator.findall(".//individualName")
            for individualName in individualNames:
                givenNames = individualName.findall(".//givenName")
                given_names = list()
                for givenName in givenNames:
                    name = flatten(givenName)
                    given_names.append(name.strip())
                surName = individualName.find(".//surName")
                sur_name = flatten(surName)
                individual_name = IndividualName(givenName=given_names,
                                                 surName=sur_name.strip())
                individual_names.append(individual_name)
            organization_names = list()
            organizationNames = creator.findall(".//organizationName")
            for organizationName in organizationNames:
                organization_name = flatten(organizationName)
                organization_names.append(organization_name.strip())
            position_names = list()
            positionNames = creator.findall(".//positionName")
            for positionName in positionNames:
                position_name = flatten(positionName)
                position_names.append(position_name.strip())
            C = Creator(individualName=individual_names,
                        organizationName=organization_names,
                        positionName=position_names)
            c.append(C)
        return c

    def _get_title(self):
        title = ""
        _ = self._root.find(".//title")
        if _ is not None:
            title = clean(_.xpath("string()"))
        return title

    def _get_pubdate(self):
        pubdate = ""
        _ = self._root.find(".//pubDate")
        if _ is not None:
            pubdate = clean(_.xpath("string()"))
        return pubdate

    @property
    def creators(self):
        return self._creators

    @property
    def title(self):
        return self._title

    @property
    def pubdate(self):
        return self._pubdate


def main():
    return 0


if __name__ == "__main__":
    main()
