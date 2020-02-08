#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: style

:Synopsis:
    Generates a stylized PASTA data package citation for the given style.

:Author:
    servilla

:Created:
    1/27/20
"""
import json

import daiquiri
import pendulum

from webapp.exceptions import StyleError
from webapp.utils import doi_url
from webapp.utils import initials
from webapp.utils import pub_year


logger = daiquiri.getLogger(__name__)


class Stylizer(object):
    def __init__(self, citation: dict):
        self._citation = citation

    def stylize(self, style: str, pid: str, access: str) -> dict:
        style = style.upper()
        if style in styles:
            stylizer = styles[style]
            if style in ('BIBTEX', "BIBTEX-ONLINE"):
                stylized = stylizer(pid, access, self._citation)
            elif style in ('ESIP'):
                stylized = stylizer(access, self._citation)
            else:
                stylized = stylizer(self._citation)
            return stylized
        else:
            msg = f"Requested style not supported: {style}"
            raise StyleError(msg)


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


def bibtex(pid: str, access: str, citation: dict) -> dict:

    bibtext = dict()

    individuals = _individuals(citation["authors"])
    organizations = _organization(citation["authors"])
    positions = _positions(citation["authors"])

    names = list()
    for individual in individuals:
        individual[0] = " ".join([_.strip() for _ in individual[0]])
        name = f"{individual[0]} {individual[1]}"
        names.append(name.strip())
    individuals = names

    names = []
    for organization in organizations:
        names.append(f"{{{organization}}}")
    organizations = names

    authors = individuals + organizations
    if len(authors) > 0:
        stylized_authors = " and ".join(authors)
    else:
        names = []
        for position in positions:
            names.append(f"{{{position}}}")
        authors = names
        stylized_authors = " and".join(authors)

    doi = doi_url(citation['doi'])
    publisher = citation['publisher']
    title = citation['title']
    version = citation['version']
    year = pub_year(citation['pubdate'])

    bibtext["author"] = f"    author={{{stylized_authors}}}"
    bibtext["title"] = f"    title={{{{{title}. ver {version}}}}}"
    bibtext["year"] = f"    year={{{year}}}"
    bibtext["howpublished"] = f"    howpublished={{{{{publisher}}}}}"

    if access is None:
        bibtext["note"] = f"    note={{Online: {doi}}}"
    else:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD", formatter="alternative")
        bibtext["note"] = f"    note={{Online: {doi} ({now})}}"

    fields = list()
    for field in bibtext:
        fields.append(bibtext[field])

    s = ",\n".join(fields)
    stylized = {"citation": f"@misc{{{pid},\n{s}\n}}"}
    return stylized


def bibtex_online(pid: str, access: str, citation: dict) -> dict:

    bibtext = dict()

    individuals = _individuals(citation["authors"])
    organizations = _organization(citation["authors"])
    positions = _positions(citation["authors"])

    names = list()
    for individual in individuals:
        individual[0] = " ".join([_.strip() for _ in individual[0]])
        name = f"{individual[0]} {individual[1]}"
        names.append(name.strip())
    individuals = names

    names = []
    for organization in organizations:
        names.append(f"{{{organization}}}")
    organizations = names

    authors = individuals + organizations
    if len(authors) > 0:
        stylized_authors = " and ".join(authors)
    else:
        names = []
        for position in positions:
            names.append(f"{{{position}}}")
        authors = names
        stylized_authors = " and".join(authors)

    doi = doi_url(citation['doi'])
    publisher = citation['publisher']
    title = citation['title']
    version = citation['version']
    year = pub_year(citation['pubdate'])

    bibtext["author"] = f"    author={{{stylized_authors}}}"
    bibtext["title"] = f"    title={{{{{title}. ver {version}}}}}"
    bibtext["year"] = f"    year={{{year}}}"
    bibtext["version"] = f"    version={{{version}}}"
    bibtext["organization"] = f"    organization={{{{{publisher}}}}}"

    if access is None:
        bibtext["url"] = f"    url={{{doi}}}"
    else:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD",
                                           formatter="alternative")
        bibtext["url"] = f"    url={{{doi} ({now})}}"
        bibtext["timestamp"] = f"    timestamp={{{now}}}"

    fields = list()
    for field in bibtext:
        fields.append(bibtext[field])

    s = ",\n".join(fields)
    stylized = {"citation": f"@online{{{pid},\n{s}\n}}"}
    return stylized


def dryad(citation: dict) -> dict:

    stylized = dict()

    individuals = _individuals(citation["authors"])
    organizations = _organization(citation["authors"])
    positions = _positions(citation["authors"])

    names = list()
    for individual in individuals:
        given_name_initials = initials(individual[0], dot=False)
        individual[0] = given_name_initials
        name = f"{individual[1]} {individual[0]}"
        names.append(name.strip())
    individuals = names

    authors = individuals + organizations
    if len(authors) > 0:
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized_authors = " ".join(authors)
        elif len(authors) > 2:
            stylized_authors = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized_authors = author
    else:
        authors = positions
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized_authors = " ".join(authors)
        elif len(authors) > 2:
            stylized_authors = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized_authors = author

    stylized["authors"] = stylized_authors
    stylized["pub_year"] = f"({pub_year(citation['pubdate'])})"
    stylized["title"] = f"{citation['title']}."
    stylized["publisher"] = f"{citation['publisher']}."
    stylized["doi"] = doi_url(citation["doi"])

    return stylized


def esip(access: str, citation: dict) -> dict:

    stylized = dict()

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
            stylized_authors = " ".join(authors)
        elif len(authors) > 2:
            stylized_authors = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized_authors = author
    else:
        # Only add positions if no individuals or organizations
        authors = positions
        if len(authors) > 1:
            authors[-1] = f"and {authors[-1]}"
        if len(authors) == 2:
            stylized_authors = " ".join(authors)
        elif len(authors) > 2:
            stylized_authors = ", ".join(authors)
        else:
            author = authors[0].rstrip(".")
            stylized_authors = author

    stylized["authors"] = f"{stylized_authors}."
    stylized["pub_year"] = f"{pub_year(citation['pubdate'])}."
    stylized["title"] = f"{citation['title']}"
    stylized["version"] = f"ver {citation['version']}."
    stylized["publisher"] = f"{citation['publisher']}."
    stylized["doi"] = f"{doi_url(citation['doi'])}."

    if access is not None:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD",
                                           formatter="alternative")
        stylized["accessed"] = f"Accessed {now}."

    return stylized


def raw(citation: dict) -> dict:
    stylized = dict()
    stylized["citation"] = citation
    return stylized


styles = {
    "RAW": raw,
    "ESIP": esip,
    "DRYAD": dryad,
    "BIBTEX": bibtex,
    "BIBTEX-ONLINE": bibtex_online
}
