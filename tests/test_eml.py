#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_eml_parsing

:Synopsis:

:Author:
    servilla

:Created:
    1/21/20
"""
import pytest

from webapp.eml import Eml

test_eml_file = "./data/test_eml.1.1.xml"

@pytest.fixture()
def eml_str():
    with open(test_eml_file, "r") as f:
        e = f.read()
    return e


def test_eml_object(eml_str):
    eml = Eml(eml_str)
    print(eml.creators)
    assert isinstance(eml, Eml)
