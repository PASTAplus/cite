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
from webapp.utils import doi_url
from webapp.utils import initials
from webapp.utils import pub_year


logger = daiquiri.getLogger(__name__)


class Stylizer(object):
    def __init__(self, style: str):
        if style in styles:
            self._stylizer = styles[style]
        else:
            msg = f"Unrecognized style requested: {style}"
            raise StyleError(msg)


    @property
    def stylize(self):
        return self._stylizer


def esip(citation: dict, accept: str) -> str:

    stylized = list()

    individuals = list()
    authors = citation["authors"]
    for author in authors:
        individual_names = author["individual_names"]
        for individual_name in individual_names:
            given_names = individual_name["given_names"]
            given_name_initials = initials(given_names)
            sur_name = individual_name["sur_name"]
            name = f"{given_name_initials} {sur_name}"
            individuals.append(name.strip())

    organizations = list()
    authors = citation["authors"]
    for author in authors:
        individual_names = author["individual_names"]
        position_names = author["position_names"]
        organization_names = author["organization_names"]
        if len(individual_names) == 0:
            for organization_name in organization_names:
                organizations.append(organization_name)

    positions = list()
    authors = citation["authors"]
    for author in authors:
        individual_names = author["individual_names"]
        position_names = author["position_names"]
        organization_names = author["organization_names"]
        if len(individual_names) == 0 and len(organization_names) == 0:
            for position_name in position_names:
                positions.append(position_name)

    # Reverse lead author name
    if len(individuals) > 0:
        lead_individual = individuals[0]
        name = lead_individual.split(" ")
        if len(name) == 2:
            individuals[0] = f"{name[1]}, {name[0]}"

    authors = individuals + organizations
    if len(authors) > 0:
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized.append(" ".join(authors))
        elif len(authors) > 2:
            stylized.append(", ".join(authors))
        else:
            author = authors[0].rstrip(".")
            stylized.append(author)
    else:
        authors = positions
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized.append(" ".join(authors))
        elif len(authors) > 2:
            stylized.append(", ".join(authors))
        else:
            author = authors[0].rstrip(".")
            stylized.append(author)

    stylized.append(". ")
    stylized.append(pub_year(citation["pubdate"]))
    stylized.append(". ")
    stylized.append(citation["title"])
    stylized.append(". ")
    stylized.append("Version ")
    stylized.append(citation["version"])
    stylized.append(". ")
    stylized.append(citation["publisher"])
    stylized.append(". ")
    doi = doi_url(citation["doi"])
    if "text/html" in accept:
        stylized.append(f"<a href='{doi}'>")
        stylized.append(doi)
        stylized.append("</a>")
    else:
        stylized.append(doi)
    stylized.append(". ")

    now = (pendulum.now("UTC")).format("D MMM YYYY", formatter="alternative")
    stylized.append("Accessed ")
    stylized.append(now)
    stylized.append(". ")

    return "".join(stylized)


styles = {
    "ESIP": esip
}
