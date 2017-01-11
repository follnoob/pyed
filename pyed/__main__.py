#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Jens Wilberg
#
# This file is part of pyed.
#
# pyed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyed.  If not, see <http://www.gnu.org/licenses/>.
"""Main Module."""
import argparse
import gettext
from . import gui

_ = gettext.gettext


def main():
    """Main."""
    parser = argparse.ArgumentParser(description=_("Simple Texteditor."))
    parser.add_argument(_("file"), metavar=_("file"), nargs='?',
                        help=_("the path to a file"))
    args = parser.parse_args()
    gui.run(args.file)


if __name__ == '__main__':
    main()
