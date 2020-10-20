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
"""Implementation of panels."""
import math
import os
import re

import wx
import wx.adv
import wx.stc

from pyed.gui.Dialog import GotoDialog

_ = wx.GetTranslation


class WritePanel(wx.Panel):
    """Class of the main Panel.

    Parameters
    ----------
    filename : str
        The filename of the current file
    font : wx.Font
        The default font for the widgets

    The MainPanel takes the same arguments as the wx.Panel class.
    """

    def __init__(self, filename, font, *args, **kwargs):
        """init."""
        super(WritePanel, self).__init__(*args, **kwargs)
        self.path = None
        self.filename = filename

        # don't set window to modified when loding a file
        self.fileLoaded = False
        self.lastSearch = (0, 0)
        self.numberSize = 12

        # widgets
        self.text = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)
        self.text.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.text.SetMarginWidth(1, 0)
        self.text.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        self.text.StyleClearAll()

        # Eventhandler
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.text.Bind(wx.stc.EVT_STC_MODIFIED, self.onModify)
        self.text.Bind(wx.stc.EVT_STC_UPDATEUI, self.updateLineCol)

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND, 1)
        self.SetSizerAndFit(sizer)

    ## EventHandler ##
    def onClose(self, event):
        """Close the panel."""
        if self.text.IsModified():
            parent = self.GetParent()
            retval = parent.showDlg(parent, _("There are unsaved changes.\n Do you want to save"),
                                    _("Unsaved Changes"), wx.YES_NO | wx.YES_DEFAULT)

            if retval == wx.ID_YES:
                self.saveFile()

        self.Destroy()

    def onModify(self, event):
        """Shows in title if text is modified."""
        if self.fileLoaded:
            event.Skip()
            return

        self.GetParent().SetTitle("*%s - pyed" % (self.filename))

        if self.text.GetMarginWidth(1) > 0:
            digits = int(math.log10(self.text.GetLineCount())) + 1
            self.text.SetMarginWidth(1, self.numberSize * digits)

        event.Skip()

    def updateLineCol(self, event):
        """Updates the line and col number on statusbar."""
        bl, column, line = self.text.PositionToXY(
            self.text.GetInsertionPoint())
        status = "Line: %d Column: %d" % (line + 1, column)
        statusbar = self.GetParent().GetStatusBar()
        statusbar.SetStatusText(status, 1)

        # change the size of the statusbar column
        font = statusbar.GetFont()
        dc = wx.WindowDC(statusbar)
        dc.SetFont(font)
        width, height = dc.GetTextExtent(status)

        # The statusbar needs to be wider to prevent elipsis
        width += font.GetPixelSize().GetWidth() * 4
        statusbar.SetStatusWidths([-1, width])

    ## Methods ##
    def openFile(self, filepath):
        """This function opens the given file.

        Parameters
        ----------
        filepath: str
            path to the file
        """
        self.fileLoaded = True

        if os.path.exists(filepath):
            self.text.LoadFile(filepath)

        self.fileLoaded = False
        self.path = filepath
        self.filename = os.path.basename(filepath)

    def saveFile(self):
        """This function saves the current file."""
        try:
            self.text.SaveFile(self.path)
            self.GetParent().SetTitle("%s - pyed" % (self.filename))
            self.text.SetSavePoint()
        except TypeError:
            self.saveFileAs()

    def saveFileAs(self):
        """Open save file dialog."""
        parent = self.GetParent()
        fdlg = wx.FileDialog(parent, _("Save As"), os.getcwd(), "",
                             "*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if fdlg.ShowModal() == wx.ID_OK:
            self.path = fdlg.GetPath()
            self.text.SaveFile(self.path)
            self.filename = fdlg.GetFilename()
            parent.SetTitle("%s - pyed" % (self.filename))
            self.text.SetSavePoint()

    def hasSelection(self):
        """Check if something is selected.

        Returns
        -------
        bool
            True if something is selected. Else False
        """
        return True if self.text.GetSelectedText() else False

    def undo(self):
        """Undo the last changes."""
        self.text.Undo()

    def redo(self):
        """Redo the last changes."""
        self.text.Redo()

    def cut(self):
        """Cuts the selection to the clipboard."""
        self.text.Cut()

    def copy(self):
        """Copies the selection to the clipboard."""
        self.text.Copy()

    def paste(self):
        """Paste from the clipboard."""
        self.text.Paste()

    def selectAll(self):
        """Select all text in the entire document."""
        self.text.SelectAll()

    def find(self, flags, findStr=""):
        """Find a string in the text.

        Parameters
        ----------
        flags : int
            The sum of flags for the search
        findStr : str
            The string to search. If empty, the selected string is used
        """
        if not findStr:
            findStr = self.text.GetSelectedText()

        if flags & 1:
            self.text.SearchAnchor()
            self.text.SearchPrev(flags, findStr)
        else:
            self.lastSearch = (self.text.GetInsertionPoint(),
                               self.text.GetAnchor())
            self.text.SetInsertionPoint(sum(self.lastSearch))
            self.text.SearchAnchor()
            searchVal = self.text.SearchNext(flags, findStr)

            if searchVal < 0:
                self.text.SetSelection(*self.lastSearch)
                self.text.SetAnchor(self.lastSearch[0])

        self.text.EnsureCaretVisible()

    def replace(self, replaceStr, findStr):
        """Replaces the found string with replaceStr.

        Parameters
        ----------
        replaceStr : str
            String which replaces the found string
        findStr : str
            The string to search
        """
        select = self.text.GetSelectedText()

        if select == findStr:
            self.text.ReplaceSelection(replaceStr)

    def replaceAll(self, replaceStr, findStr):
        """Replaces all findStr with replaceStr.

        Parameters
        ----------
        replaceStr : str
            String which replaces the found string
        findStr : str
            The string to search
        """
        text = self.text.GetValue()
        # Find start position
        positions = [m.start() for m in re.finditer(findStr, text)]

        for start in positions:
            self.text.Replace(start, start + len(findStr), replaceStr)

    def resetSearch(self):
        """Resets the search."""
        self.lastSearch = (0, 0)

    def setFont(self, font):
        """Set font of the textctrl.

        Parameters
        ----------
        font : wx.Font
            The font
        """
        self.text.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        self.text.StyleClearAll()

    def goto(self):
        """Goto line and column.

        This functions opens a goto dialog.
        """
        lines = self.text.LineCount
        columns = len(self.text.GetLineText(0))

        with GotoDialog(self, wx.ID_ANY, (lines, columns)) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                line, column = dlg.GetValue()
                position = self.text.XYToPosition(column, line)

                # SetInsertionPoint Selects the text between the position from
                # the old curser to the new curser so we use SetSelection with
                # only the new position
                self.text.SetSelection(position, position)

    def getFont(self):
        """Returns the current font of the textctrl.

        Returns
        -------
        wx.Font
        """
        return self.text.StyleGetFont(wx.stc.STC_STYLE_DEFAULT)

    def showLineNumbers(self):
        """Shows the line number on the left side."""
        if self.text.GetMarginWidth(1) > 0:
            self.text.SetMarginWidth(1, 0)
        else:
            digits = int(math.log10(self.text.GetLineCount())) + 1
            self.text.SetMarginWidth(1, self.numberSize * digits)
