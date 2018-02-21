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
"""GUI for pyed."""
import os
import re
import codecs
import json
import math

import wx
import wx.adv
import wx.stc

from .__version__ import VERSION_STRING

_ = wx.GetTranslation
__version__ = VERSION_STRING


class WritePanel(wx.Panel):

    def __init__(self, filename, font, *args, **kwargs):
        """Class of the main Panel.

        Parameters
        ----------
        filename : str
            The filename of the current file
        font : wx.Font
            The default font for the widgets

        The MainPanel takes the same arguments as the wx.Panel class.
        """
        super(WritePanel, self).__init__(*args, **kwargs)
        # stuff
        self.path = None
        self.filename = filename
        self.fileLoaded = False  # don't set window to modified when loding a file
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
        """Close the panel"""
        if self.text.IsModified():
            parent = self.GetParent()
            retval = parent.showDlg(parent, _("There are unsaved changes.\n Do you want to save"),
                                    _("Unsaved Canges"), wx.YES_NO | wx.YES_DEFAULT)
            if retval == wx.ID_YES:
                self.saveFile()
        self.Destroy()

    def onModify(self, event):
        """Schows in title if text is modified."""
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
        bl, c, l = self.text.PositionToXY(self.text.GetInsertionPoint())
        status = "Line: %d Column: %d" % (l + 1, c)
        statusbar = self.GetParent().GetStatusBar()
        statusbar.SetStatusText(status, 1)
        # ugly method to change the size of a statusbar column
        font = statusbar.GetFont()
        dc = wx.WindowDC(statusbar)
        dc.SetFont(font)
        width, height = dc.GetTextExtent(status)
        statusbar.SetStatusWidths([-1, width + 30])

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
        fdlg = wx.FileDialog(parent, _("Save As"),
                             os.getcwd(), "", "*", wx.FD_SAVE |
                             wx.FD_OVERWRITE_PROMPT)
        if fdlg.ShowModal() == wx.ID_OK:
            self.path = fdlg.GetPath()
            self.text.SaveFile(self.path)
            self.filename = fdlg.GetFilename()
            parent.SetTitle("%s - pyed" % (self.filename))
            self.text.SetSavePoint()

    def hasSelection(self):
        """Check if somthing is selected.

        Returns
        -------
        bool
            True if somthing is selected. Elese False
        """
        return True if self.text.GetSelectedText() else False

    def undo(self):
        """Undo the last changes."""
        self.text.Undo()

    def redo(self):
        """Redo the last changes."""
        self.text.Redo()

    def cut(self):
        """Cuts the selection to the clipbord."""
        self.text.Cut()

    def copy(self):
        """Copies the selection to the clipbord."""
        self.text.Copy()

    def paste(self):
        """Paste from the clipbord."""
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
            String wich replaces the found string
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
            String wich replaces the found string
        findStr : str
            The string to search
        """
        text = self.text.GetValue()
        # Find start position
        positions = [m.start()
                     for m in re.finditer(findStr, text)]
        for start in positions:
            self.text.Replace(start, start + len(findStr), replaceStr)

    def resetSearch(self):
        """Resets the search"""
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

    def getFont(self):
        """Returns the current font of the textctrl.

        Returns
        -------
        wx.Font
        """
        return self.text.StyleGetFont(wx.stc.STC_STYLE_DEFAULT)

    def showLineNumbers(self):
        """Shwos the line nnumber on the left side."""
        if self.text.GetMarginWidth(1) > 0:
            self.text.SetMarginWidth(1, 0)
        else:
            digits = int(math.log10(self.text.GetLineCount())) + 1
            self.text.SetMarginWidth(1, self.numberSize * digits)


class MainFrame(wx.Frame):

    def __init__(self, filepath=None, *args, **kwargs):
        """Class for the MainFrame.

        The MainFrame takes the same arguments as the wx.Frame class.
        """
        super(MainFrame, self).__init__(*args, **kwargs)
        # stuff
        self.newFileCounter = 1
        filename = _("Untitled %d" % (self.newFileCounter))
        userHome = os.path.expanduser('~')
        confDir = os.path.join(userHome, ".config", "pyed")
        self.settingsPath = os.path.join(confDir, "settings.json")
        if not os.path.exists(confDir):
            os.mkdir(confDir)
        defaultFont = wx.Font(
            12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Monospace")
        self.settings = {"font": str(defaultFont.GetNativeFontInfo()),
                         "show_line_numbers": False}
        if os.path.exists(self.settingsPath):
            with codecs.open(self.settingsPath, "r", "utf-8") as f:
                self.settings = json.load(f)
            defaultFont = wx.Font(self.settings["font"])
            # widgets
        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-1, 125])
        self.writePanel = WritePanel(
            filename, defaultFont, self)

        # open file from cli
        if filepath:
            self.writePanel.openFile(filepath)
            filename = os.path.basename(filepath)
        self.SetTitle("%s - pyed" % (filename))

        # create menu
        filemenu = wx.Menu()
        editmenu = wx.Menu()
        searchmenu = wx.Menu()
        helpmenu = wx.Menu()
        viewmenu = wx.Menu()

        menuNew = filemenu.Append(wx.ID_NEW, _("New"), _(" Create new file"))
        menuOpen = filemenu.Append(wx.ID_OPEN, _("Open"), _(" Open file"))
        filemenu.AppendSeparator()
        menuSave = filemenu.Append(wx.ID_SAVE, _("Save"), _(" Save file"))
        menuSaveAs = filemenu.Append(
            wx.ID_SAVEAS, _("Save As"), _(" Save file as"))
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, _("Exit"), _(" Exit Program"))
        menuAbout = helpmenu.Append(wx.ID_ABOUT,
                                    _("About"), _(" Infos about this program"))

        menuUndo = editmenu.Append(wx.ID_UNDO, _(
            "Undo\tCTRL+Z"), _(" Undo the last action"))
        menuRedo = editmenu.Append(wx.ID_REDO, _(
            "Redo\tCTRL+Y"), _(" Redo the last action"))
        editmenu.AppendSeparator()
        self.menuCut = editmenu.Append(wx.ID_CUT, _(
            "Cut"), _(" Cut the selection"))
        self.menuCopy = editmenu.Append(wx.ID_COPY, _(
            "Copy"), _(" Copy the selection"))
        menuPaste = editmenu.Append(wx.ID_PASTE, _(
            "Paste"), _(" Paste the clipbord"))
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, _(
            "Select All"), _(" Select the text in the entire document"))

        menuFind = searchmenu.Append(
            wx.ID_FIND, _("Find"), _(" Search for text"))
        menuFindNext = searchmenu.Append(
            wx.ID_ANY, _("Find Next\tCTRL+G"), _(" Search forwards for the same text"))
        menuFindPrev = searchmenu.Append(
            wx.ID_ANY, _("Find Previous\tSHIFT+CTRL+G"), _(" Search backwards for the same text"))
        menuFindRep = searchmenu.Append(
            wx.ID_REPLACE, _("Find and Replace"), _(" Search for and replace text"))

        menuFont = viewmenu.Append(wx.ID_SELECT_FONT, _(
            "Select Font"), _(" Change the editor font"))
        menuLineNumber = viewmenu.Append(wx.ID_ANY, _("Show Line Numbers"),
                                         _(" Shows the line numbers on the left side"),
                                         kind=wx.ITEM_CHECK)

        # create menubar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, _("&File"))
        menubar.Append(editmenu, _("&Edit"))
        menubar.Append(searchmenu, _("&Search"))
        menubar.Append(viewmenu, _("&View"))
        menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(menubar)

        # Eventhandler
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.onNew, menuNew)
        self.Bind(wx.EVT_MENU, self.onSave, menuSave)
        self.Bind(wx.EVT_MENU, self.onSaveAs, menuSaveAs)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        editmenu.Bind(wx.EVT_MENU_OPEN, self.onEdit)
        self.Bind(wx.EVT_MENU, self.onUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.onRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.onCut, self.menuCut)
        self.Bind(wx.EVT_MENU, self.onCopy, self.menuCopy)
        self.Bind(wx.EVT_MENU, self.onPaste, menuPaste)
        self.Bind(wx.EVT_MENU, self.onSelectAll, menuSelectAll)

        self.Bind(wx.EVT_MENU, self.onSearch, menuFind)
        self.Bind(wx.EVT_MENU, self.onSearchNext, menuFindNext)
        self.Bind(wx.EVT_MENU, self.onSearchPrev, menuFindPrev)
        self.Bind(wx.EVT_MENU, self.onSearchAndReplace, menuFindRep)

        self.Bind(wx.EVT_MENU, self.onSelectFont, menuFont)
        self.Bind(wx.EVT_MENU, self.onShowLines, menuLineNumber)

        self.Bind(wx.EVT_FIND, self.onFind)
        self.Bind(wx.EVT_FIND_NEXT, self.onFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.onReplace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.onReplaceAll)
        self.Bind(wx.EVT_FIND_CLOSE, self.onFindClose)

        # Accelerator Table
        table = []
        eventId = wx.NewId()
        table.append((wx.ACCEL_CTRL, ord('Z'), eventId))
        self.Bind(wx.EVT_MENU, self.onUndo, id=eventId)
        eventId = wx.NewId()
        table.append((wx.ACCEL_CTRL, ord('Y'), eventId))
        self.Bind(wx.EVT_MENU, self.onRedo, id=eventId)
        eventId = wx.NewId()
        table.append((wx.ACCEL_CTRL, ord('F'), eventId))
        self.Bind(wx.EVT_MENU, self.onSearch, id=eventId)
        eventId = wx.NewId()
        table.append((wx.ACCEL_SHIFT | wx.ACCEL_CTRL, ord('G'), eventId))
        self.Bind(wx.EVT_MENU, self.onSearchPrev, id=eventId)
        eventId = wx.NewId()
        table.append((wx.ACCEL_CTRL, ord('F'), eventId))
        self.Bind(wx.EVT_MENU, self.onSearch, id=eventId)
        # eventId = wx.NewId()
        # table.append((wx.ACCEL_CTRL, ord('R'), eventId))
        # self.Bind(wx.EVT_MENU, self.onSearchAndReplace, id=eventId)
        accTable = wx.AcceleratorTable(table)
        self.SetAcceleratorTable(accTable)
        if self.settings["show_line_numbers"]:
            menuLineNumber.Check()
            self.writePanel.showLineNumbers()

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.writePanel, 1, wx.EXPAND, 1)
        self.SetSizer(sizer)

    ## EventHandler ##
    def onExit(self, event):
        """Handel exit event."""
        self.writePanel.Close()
        self.Destroy()

    def onAbout(self, event):
        """Shows informations about this program."""
        description = _("""pyed is a simple Texteditor""")

        licence = """pyed is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyed is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/."""

        info = wx.adv.AboutDialogInfo()
        info.SetName('pyed')
        info.SetVersion(__version__)
        info.SetDescription(description)
        info.SetCopyright('Copyright (C) 2017 Jens Wilberg')
        info.SetLicence(licence)
        info.AddDeveloper("Jens Wilberg <jens_wilberg@outlook.com>")
        wx.adv.AboutBox(info)

    def onNew(self, event):
        """"Creates a new file."""
        self.writePanel.Close()
        self.newFileCounter += 1
        filename = _("Untitled %d" % (self.newFileCounter))
        self.writePanel = WritePanel(
            filename, wx.Font(self.settings["font"]), self)
        self.SetTitle("%s - pyed" % (filename))
        self.GetSizer().Add(self.writePanel, 1, wx.EXPAND, 1)
        self.Layout()
        self.writePanel.SetFocus()

    def onOpen(self, event):
        """Open a file."""
        # The filedialog is here becaus I change the panel
        fdlg = wx.FileDialog(self, _("Choose file"),
                             os.getcwd(), "", "*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fdlg.ShowModal() == wx.ID_OK:
            self.writePanel.Close()
            filename = fdlg.GetFilename()
            self.writePanel = WritePanel(filename, self)
            self.SetTitle("%s - pyed" % (filename))
            self.writePanel.openFile(fdlg.GetPath())
            self.GetSizer().Add(self.writePanel, 1, wx.EXPAND, 1)
            self.Layout()
            self.writePanel.SetFocus()
        fdlg.Destroy()

    def onSave(self, event):
        """Save current file."""
        self.writePanel.saveFile()

    def onSaveAs(self, event):
        """Opens save as dialog."""
        self.writePanel.saveFileAs()

    def onEdit(self, event):
        """Handles edit menu event."""
        if self.writePanel.hasSelection():
            self.menuCut.Enable(True)
            self.menuCopy.Enable(True)
        else:
            self.menuCut.Enable(False)
            self.menuCopy.Enable(False)

    def onUndo(self, event):
        """Undos the last Changes in the current writePanel."""
        self.writePanel.undo()

    def onRedo(self, event):
        """Redos the last Changes in the current writePanel."""
        self.writePanel.redo()

    def onCut(self, event):
        """Handles cut event."""
        self.writePanel.cut()

    def onCopy(self, event):
        """Handles copy event."""
        self.writePanel.copy()

    def onPaste(self, event):
        """Handles paste event."""
        self.writePanel.paste()

    def onSelectAll(self, event):
        """Handles select all event."""
        self.writePanel.selectAll()

    def onSearch(self, event):
        """Handles the event if you want to search."""
        data = wx.FindReplaceData()
        dlg = wx.FindReplaceDialog(self, data, _("Find"))
        dlg.data = data  # prevent segmentation faults
        dlg.Show()

    def onSearchAndReplace(self, event):
        """Opens search and replace dialog."""
        data = wx.FindReplaceData()
        dlg = wx.FindReplaceDialog(self, data, _(
            "Find and Replace"), style=wx.FR_REPLACEDIALOG)
        dlg.data = data  # prevent segmentation faults
        dlg.Show()

    def onSearchNext(self, event):
        """Handles the events from the 'Find Next'."""
        self.writePanel.find(0)

    def onSearchPrev(self, event):
        """Handles the events from the 'Find Previous'."""
        self.writePanel.find(1)

    def onFind(self, event):
        """Handles the events of the FindReplaceDialog."""
        findStr = event.GetFindString()
        flags = event.GetFlags()
        self.writePanel.find(flags, findStr)

    def onReplace(self, event):
        """Handles replace event."""
        replaceStr = event.GetReplaceString()
        findStr = event.GetFindString()
        self.writePanel.replace(replaceStr, findStr)

    def onReplaceAll(self, event):
        """Handles replace all event."""
        replaceStr = event.GetReplaceString()
        findStr = event.GetFindString()
        self.writePanel.replaceAll(replaceStr, findStr)

    def onFindClose(self, event):
        """Handles the close event of the FindReplaceDialog."""
        dlg = event.GetEventObject()
        dlg.Destroy()
        self.writePanel.resetSearch()

    def onSelectFont(self, event):
        """Select a new font."""
        fontData = wx.FontData()
        font = self.writePanel.getFont()
        fontData.SetInitialFont(font)
        fontDlg = wx.FontDialog(self, fontData)
        if fontDlg.ShowModal() == wx.ID_OK:
            # forward wx.FontData from fontDlg because if I use the variable
            # fontData to get the font it throws invalid font errors.
            font = fontDlg.GetFontData().GetChosenFont()
            self.settings["font"] = str(font.GetNativeFontInfo())
            self.saveSettings()
            self.writePanel.setFont(font)

    def onShowLines(self, event):
        """Shows line numbers."""
        self.writePanel.showLineNumbers()
        if not self.settings["show_line_numbers"]:
            self.settings["show_line_numbers"] = True
        else:
            self.settings["show_line_numbers"] = False
        self.saveSettings()

    ## Methods ##
    def showDlg(self, parent, message, title, style):
        """Displays a dialog."""
        dlg = wx.MessageDialog(parent=parent, message=message,
                               caption=title, style=style)
        retval = dlg.ShowModal()
        dlg.Destroy()
        return retval

    def saveSettings(self):
        """Saves the settings."""
        with codecs.open(self.settingsPath, "w+", "utf-8") as of:
            json.dump(self.settings, of)
