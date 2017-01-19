# pyed

Pyed is a simple text editor written in Python3 with the wxPython Phoenix
framework. I think the editor is now usable, so I updated it to beta status.
Pleas open an issue for every bug you found.

## Installation

There is no installation required. The only thing you need is Python3
and [wxPython Phoenix](https://github.com/wxWidgets/Phoenix).

only tested on Python 3.5.

Supported operatingsystems:

- Linux (Main development on Mint 18)
- Windows (Tested on Windows 10, see [bugs](#bugs) for more information)

## Usage

you can start pyed with the following command:

    python3 pyed.py

## Things i maybe implement

- Toolbar
- Multiple files in tab view
- Basic syntax highlighting

## Known Bugs

- The horizontal scrollbar has an odd behavior (standard in wx.stc.StyledTextCtrl)
- Linux Mint 18: Black line at the left site
- Windows: no support of wx default shortcuts and images

## Author and License

Copyright (C) Jens Wilberg Jannuary 2017

    pyed is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyed is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyed.  If not, see <http://www.gnu.org/licenses/>.

    The R script can be used, copied and modified under the terms of the GNU
    General Public License version 2.
