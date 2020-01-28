#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: exceptions

:Synopsis:

:Author:
    servilla

:Created:
    1/27/20
"""

class StyleError(Exception):
    """Raised when a citation style error occurs
    Args:
        msg (str): explanation of the error
    """


class FormatError(Exception):
    """Raised when a citation format error occurs
    Args:
        msg (str): explanation of the error
    """