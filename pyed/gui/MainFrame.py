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
"""Pyeds Mainframe."""
import json
import os

import wx

from pyed.__version__ import VERSION_STRING
from pyed.gui.Panel import WritePanel

_ = wx.GetTranslation
__version__ = VERSION_STRING


class MainFrame(wx.Frame):
    """Class for the MainFrame.

    The MainFrame takes the same arguments as the wx.Frame class.
    """

    def __init__(self, filepath=None, *args, **kwargs):
        """init."""
        super(MainFrame, self).__init__(*args, **kwargs)
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
            with open(self.settingsPath, "r", encoding="utf-8") as f:
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
            "Paste"), _(" Paste the clipboard"))
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, _(
            "Select All"), _(" Select the text in the entire document"))

        menuFind = searchmenu.Append(
            wx.ID_FIND, _("Find"), _(" Search for text"))
        menuFindNext = searchmenu.Append(wx.ID_ANY, _("Find Next\tCTRL+G"),
                                         _(" Search forwards for the same text"))
        menuFindPrev = searchmenu.Append(
            wx.ID_ANY, _("Find Previous\tSHIFT+CTRL+G"),
            _(" Search backwards for the same text"))
        menuFindRep = searchmenu.Append(
            wx.ID_REPLACE, _("Find and Replace"),
            _(" Search for and replace text"))
        searchmenu.AppendSeparator()
        menuGoto = searchmenu.Append(wx.ID_PREVIEW_GOTO, _(
            "Go to.."), _(" Go to a specific location in the document"))

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
        self.Bind(wx.EVT_MENU, self.onGoTo, menuGoto)

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
        """Creates a new file."""
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
        # The filedialog is here because I change the panel
        fdlg = wx.FileDialog(self, _("Choose file"), os.getcwd(), "",
                             "*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

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
        """Undoes the last Changes in the current writePanel."""
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
        dlg = wx.FindReplaceDialog(self, data, _("Find and Replace"), style=wx.FR_REPLACEDIALOG)
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

    def onGoTo(self, event):
        """Handels goto event."""
        self.writePanel.goto()

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
        with open(self.settingsPath, "w+", encoding="utf-8") as of:
            json.dump(self.settings, of)
