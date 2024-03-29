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

    def stylize(self, style: str, pid: str, access: bool, no_dot: bool) -> dict:
        style = style.upper()
        if style in styles:
            stylizer = styles[style]
            if style in ('BIBTEX', "BIBTEX-ONLINE"):
                stylized = stylizer(self._citation, pid, access)
            elif style in 'ESIP':
                stylized = stylizer(self._citation, access, no_dot)
            else:
                stylized = stylizer(self._citation)
            return stylized
        else:
            msg = f"Requested style not supported: {style}"
            raise StyleError(msg)


def _names(authors: list) -> list:
    """_names

    Build a list of author names using the following logic:
        1. Use individual(s), ignore all organization or position names
           in creator element; otherwise
        2. Use organization(s), ignore all position names in creator element;
           otherwise
        3. Use position(s)
    :param authors: list of authors from citation data
    :return: list of names in the form [[list], str]
    """
    names = list()
    for author in authors:
        individual_names = author["individual_names"]
        organization_names = author["organization_names"]
        position_names = author["position_names"]
        if len(individual_names) != 0:
            for individual_name in individual_names:
                given_names = individual_name["given_names"]
                sur_name = individual_name["sur_name"]
                name = [given_names, sur_name]
                names.append(name)
        elif len(organization_names) != 0:
            organization_names = author["organization_names"]
            for organization_name in organization_names:
                name = [[], organization_name]
                names.append(name)
        else:
            for position_name in position_names:
                name = [[], position_name]
                names.append(name)
    return names


def bibtex(citation: dict, pid: str, access: bool) -> dict:

    bibtext = dict()

    authors = list()
    names = _names(citation["authors"])
    for name in names:
        _ = " ".join([_.strip() for _ in name[0]])
        author = f"{_} {name[1]}"
        authors.append(author.strip())
    stylized_authors = " and ".join(authors)

    doi = doi_url(citation['doi'])
    publisher = citation['publisher']
    title = citation['title']
    version = citation['version']
    year = pub_year(citation['pubdate'])

    bibtext["author"] = f"    author={{{stylized_authors}}}"
    bibtext["title"] = f"    title={{{{{title}. ver {version}}}}}"
    bibtext["year"] = f"    year={{{year}}}"
    bibtext["publisher"] = f"    publisher={{{publisher}}}"
    bibtext["doi"] = f"    doi={{{doi.replace('https://doi.org/', '')}}}"
    bibtext["url"] = f"    url={{{doi}}}"

    if access:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD")
        bibtext["urldate"] = f"    urldate={{{now}}}"

    bibtext["note"] = f"    note = {{Type: dataset}}"

    fields = list()
    for field in bibtext:
        fields.append(bibtext[field])

    s = ",\n".join(fields)
    stylized = {"citation": f"@misc{{{pid},\n{s}\n}}"}
    return stylized


def bibtex_online(citation: dict, pid: str, access: bool) -> dict:

    bibtext = dict()

    authors = list()
    names = _names(citation["authors"])
    for name in names:
        _ = " ".join([_.strip() for _ in name[0]])
        author = f"{_} {name[1]}"
        authors.append(author.strip())
    stylized_authors = " and ".join(authors)

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

    if access:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD")
        bibtext["url"] = f"    url={{{doi} ({now})}}"
        bibtext["timestamp"] = f"    timestamp={{{now}}}"
    else:
        bibtext["url"] = f"    url={{{doi}}}"

    fields = list()
    for field in bibtext:
        fields.append(bibtext[field])

    s = ",\n".join(fields)
    stylized = {"citation": f"@online{{{pid},\n{s}\n}}"}
    return stylized


def dryad(citation: dict) -> dict:

    stylized = dict()

    authors = list()
    names = _names(citation["authors"])
    for name in names:
        # Make initials if given names present
        _initials = initials(name[0], dot=False)
        _ = f"{name[1]} {_initials}"
        authors.append(_.strip())

    if len(authors) > 1:
        authors[-1] = f"and {authors[-1]}"

    if len(authors) == 2:
        stylized_authors = " ".join(authors)
    elif len(authors) > 2:
        stylized_authors = ", ".join(authors)
    else:
        stylized_authors = authors[0]

    stylized["authors"] = stylized_authors
    stylized["pub_year"] = f"({pub_year(citation['pubdate'])})"
    stylized["title"] = f"{citation['title']}."
    stylized["publisher"] = f"{citation['publisher']}."
    stylized["doi"] = doi_url(citation["doi"])

    return stylized


def esip(citation: dict, access: bool, no_dot: bool) -> dict:

    stylized = dict()

    authors = list()
    names = _names(citation["authors"])

    # Make initials if valid given names present
    for name in names:
        # Clean empty given names from list
        name[0] = [_.strip() for _ in name[0] if _ != ""]
        _initials = initials(name[0], dot=True)
        _ = f"{_initials} {name[1]}"
        authors.append(_.strip())

    # Reverse lead author name if given name present
    if len(authors) > 0 and len(names[0][0]) != 0:
        name = authors[0].split(" ")
        if len(name) >= 2:
            authors[0] = f"{' '.join(name[1:])}, {name[0]}"

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
    if no_dot:
        stylized["doi"] = f"{doi_url(citation['doi'])}"
    else:
        stylized["doi"] = f"{doi_url(citation['doi'])}."

    if access:
        now = (pendulum.now("UTC")).format("YYYY-MM-DD")
        if no_dot:
            stylized["accessed"] = f"(Accessed {now})."
        else:
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
