#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_citation

:Synopsis:

:Author:
    servilla

:Created:
    1/25/20
"""
import json

import pytest

from webapp.citation import Citation


def test_citation():
    pid = "knb-lter-nin.1.1"
    env = "production"
    style = "ESIP"
    accept = "text/plain"
    access = True
    ignores = list()
    no_dot = True
    citation = Citation(pid, env, style, accept, access, ignores, no_dot)
    assert isinstance(citation, Citation)
    assert citation.base is not None
    print(json.dumps(citation.base, indent=2))
    print(citation.formatted)
