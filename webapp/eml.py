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
        self._given_name = self._get_given_name()
        self._org_name = self._get_org_name()

    def _get_surname(self):
        surname = None
        _ = self._creator.find(".//individualName/surName")
        if _ is not None:
            surname = clean(_.text)
        return surname

    def _get_given_name(self):
        given_name = None
        _ = self._creator.find(".//individualName/givenName")
        if _ is not None:
            given_name = clean(_.text)
        return given_name

    def _get_org_name(self):
        org_name = None
        _ = self._creator.find(".//organizationName")
        if _ is not None:
            org_name = clean(_.text)
        return org_name

    @property
    def surname(self):
        return self._surname

    @property
    def given_name(self):
        return self._given_name

    @property
    def org_name(self):
        return self._org_name

class Eml(object):
    def __init__(self, eml: str):
        self._eml = eml.encode("utf-8")
        self._root = etree.fromstring(self._eml)
        self._title = self._get_title()
        self._pubdate = self._get_pubdate()
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
