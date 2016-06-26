#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import logging

from .cli import SMSSender

__all__ = ["SMSSender"]

logging.basicConfig()
log = logging.getLogger("najdisi_sms")
log.setLevel(logging.INFO)
