#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: utils

:Synopsis:

:Author:
    servilla

:Created:
    1/23/20
"""
import daiquiri

logger = daiquiri.getLogger(__name__)


def pid_triple(pid: str) -> tuple:
    _ = pid.strip().split(".")
    scope = str(_[0])
    identifier = int(_[1])
    revision = int(_[2])
    return scope, identifier, revision
