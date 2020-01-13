#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: eml

:Synopsis:

:Author:
    servilla

:Created:
    01/11/2020
"""
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


class Creator(object):
    def __init__(self, creator):
        self._creator = creator
        self._surname = self._get_surname()
        self._given_name = None
        self._org_name = None

    def _get_surname(self):
        surname = None
        _ = self._creator.find(".//individualName/surName")
        if _ is not None:
            surname = clean(_.text)
        return surname

    @property
    def surname(self):
        return self._surname


class Eml(object):
    def __init__(self, eml: str):
        self._eml = eml.encode("utf-8")
        self._root = etree.fromstring(self._eml)
        self._title = self._get_title()
        self._creators = self._get_creators()

    def _get_creators(self):
        creators = list()
        _ = self._root.findall(".//dataset/creator")
        for c in _:
            creator = Creator(c)
            creators.append(creator)
        return creators

    def _get_title(self):
        title = ""
        _ = self._root.find(".//title")
        if _ is not None:
            title = clean(_.xpath("string()"))
        return title

    @property
    def creators(self):
        return self._creators

    @property
    def title(self):
        return self._title


def main():
    return 0


if __name__ == "__main__":
    main()
