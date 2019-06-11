#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2018-2019 Nekoka.tt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in a$
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This includes various fixes to stuff in Discord.py; a paginator and navigator
to allow displaying content more than one message wide cleanly and efficiently;
many language addons such as singleton classes, async constructor classes,
collections; and a few general purpose cogs and commands such as an exec/eval
command.
"""

from . import aiojson
from .clients import *
from .commands import *
from .embeds import *
from .pag import *
from .permissions import *
from .singleton import *

__author__ = "Nekoka.tt"
__license__ = "MIT"
__url__ = "https://gitlab.com/nekokatt/nekozilla"
__version__ = "1.0.0-NEKO²-FORK"
__copyright__ = f"(c) {__author__} 2019"
