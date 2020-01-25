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
        creators = list()
        _creators = self._root.findall(".//dataset/creator")
        for _creator in _creators:
            individual_names = list()
            organization_names = list()
            position_names = list()
            _individual_names = _creator.findall(".//individualName")
            for _individual_name in _individual_names:
                given_names = list()
                _given_names = _individual_name.findall(".//givenName")
                for _given_name in _given_names:
                    given_name = (clean(_given_name.xpath("string()"))).strip()
                    given_names.append(given_name)
                _sur_name = _individual_name.find(".//surName")
                sur_name = (clean(_sur_name.xpath("string()"))).strip()
                individual_name = {"sur_name": sur_name,
                                   "given_names": given_names}
                individual_names.append(individual_name)
            _organization_names = _creator.findall(".//organizationName")
            for _organization_name in _organization_names:
                organization_name = (
                    clean(_organization_name.xpath("string()"))).strip()
                organization_names.append(organization_name)
            _position_names = _creator.findall(".//positionName")
            for _position_name in _position_names:
                position_name = (
                    clean(_position_name.xpath("string()")))
                position_names.append(position_name)
            creator = {"individual_names": individual_names,
                       "organization_names": organization_names,
                       "position_names": position_names}
            creators.append(creator)
        return creators

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
