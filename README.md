# pyed

Pyed is a simple text editor written in Python3 with the wxPython Phoenix
framework. I think the editor is now usable, so I updated it to beta status.
Pleas open an [issue](https://github.com/follnoob/pyed/issues/new) for every bug you found.

## Installation

You need to install Python3 and [wxPython Phoenix](https://github.com/wxWidgets/Phoenix)
as requirements. You can find an installation guide for Phoenix
[here](https://wiki.wxpython.org/How%20to%20install%20wxPython#Installing_wxPython-Phoenix_using_pip)

To install this package run

    make install

or

    python3 setup.py install

On Linux you can copy pyed.desktop to /usr/share/applications or ~/.local/share/applications
to integrate pyed to your menu. Also you can use this file as desktop short-cut.

only tested on Python 3.5.

Supported operating-systems:

- Linux (Main development on Mint 18)
- Windows (Tested on Windows 10)

## Usage

If you installed pyed you can start it with the command

    pyed
    
When you want to open or create a file you can use the  cli 
    
    pyed path/to/file

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
