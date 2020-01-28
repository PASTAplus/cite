#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: style

:Synopsis:

:Author:
    servilla

:Created:
    1/27/20
"""
import daiquiri
import pendulum


from webapp.exceptions import StyleError
from webapp.format import Formatter
from webapp.utils import doi_url
from webapp.utils import initials
from webapp.utils import pub_year


logger = daiquiri.getLogger(__name__)


class Stylizer(object):
    def __init__(self, citation: dict):
        self._citation = citation

    def stylize(self, style: str):
        if style in styles:
            stylizer = styles[style]
            stylized = stylizer(self._citation)
            return stylized
        else:
            msg = f"Unrecognized style requested: {style}"
            raise StyleError(msg)


def esip(citation: dict) -> dict:

    stylized = dict()

    now = (pendulum.now("UTC")).format("D MMM YYYY", formatter="alternative")

    individuals = _individuals(citation["authors"])
    organizations = _organization(citation["authors"])
    positions = _positions(citation["authors"])

    names = list()
    for individual in individuals:
        given_name_initials = initials(individual[0])
        individual[0] = given_name_initials
        name = f"{individual[0]} {individual[1]}"
        names.append(name.strip())
    individuals = names

    # Reverse lead author name
    if len(individuals) > 0:
        name = individuals[0].split(" ")
        if len(name) == 2:
            individuals[0] = f"{name[1]}, {name[0]}"

    authors = individuals + organizations
    if len(authors) > 0:
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized["authors"] = " ".join(authors)
        elif len(authors) > 2:
            stylized["authors"] = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized["authors"] = author
    else:
        authors = positions
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized["authors"] = " ".join(authors)
        elif len(authors) > 2:
            stylized["authors"] = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized["authors"] = author

    stylized["pub_year"] = pub_year(citation["pubdate"])
    stylized["title"] = citation["title"]
    stylized["version"] = f"Version {citation['version']}"
    stylized["publisher"] = citation["publisher"]
    stylized["doi"] = doi_url(citation["doi"])
    stylized["accessed"] = f"Accessed {now}"

    return stylized


styles = {
    "ESIP": esip
}


def _individuals(authors: list) -> list:
    individuals = list()
    for author in authors:
        individual_names = author["individual_names"]
        for individual_name in individual_names:
            given_names = individual_name["given_names"]
            sur_name = individual_name["sur_name"]
            name = [given_names, sur_name]
            individuals.append(name)
    return individuals


def _organization(authors: list) -> list:
    organizations = list()
    for author in authors:
        individual_names = author["individual_names"]
        position_names = author["position_names"]
        organization_names = author["organization_names"]
        if len(individual_names) == 0:
            for organization_name in organization_names:
                organizations.append(organization_name)
    return organizations


def _positions(authors: list) -> list:
    positions = list()
    for author in authors:
        individual_names = author["individual_names"]
        position_names = author["position_names"]
        organization_names = author["organization_names"]
        if len(individual_names) == 0 and len(organization_names) == 0:
            for position_name in position_names:
                positions.append(position_name)
    return positions
