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
    t = list()
    if hasattr(element, "text") and element.text is not None:
        t.append(element.text.strip())
    if hasattr(element, "__iter__"):
        for e in element:
            t.append(flatten(e))
    return (" ".join(t)).strip()


def clean(text):
    return " ".join(text.split())


Creator = namedtuple('Creator', ['individualNames', 'organizationNames',
                                 'positionNames'])
Creator.__new__.__defaults__ = (None, None, None)

IndividualName = namedtuple('IndividualName', ['givenNames', 'surName'])
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
                    name = clean(givenName.xpath("string()"))
                    given_names.append(name)
                surName = individualName.find(".//surName")
                sur_name = clean(surName.xpath("string()"))
                individual_name = IndividualName(givenNames=given_names,
                                                 surName=sur_name.strip())
                individual_names.append(individual_name)
            organization_names = list()
            organizationNames = creator.findall(".//organizationName")
            for organizationName in organizationNames:
                organization_name = clean(organizationName.xpath("string()"))
                organization_names.append(organization_name.strip())
            position_names = list()
            positionNames = creator.findall(".//positionName")
            for positionName in positionNames:
                position_name = clean(positionName.xpath("string()"))
                position_names.append(position_name)
            C = Creator(individualNames=individual_names,
                        organizationNames=organization_names,
                        positionNames=position_names)
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
