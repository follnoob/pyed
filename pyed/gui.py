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
import wx
import wx.adv
from .__version__ import VERSION_STRING

_ = wx.GetTranslation
__version__ = VERSION_STRING


class WritePanel(wx.Panel):

    def __init__(self, filename, *args, **kwargs):
        """Class of the main Panel.

        Parameters
        ----------
        filename : str
            The filename of the current file

        The MainPanel takes the same arguments as the wx.Panel class.
        """
        super(WritePanel, self).__init__(*args, **kwargs)
        # stuff
        self.path = None
        self.filename = filename
        self.fileLoaded = False

        # widgets
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # Eventhandler
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.text.Bind(wx.EVT_TEXT, self.onModify)

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND, 1)
        self.SetSizerAndFit(sizer)

    def openFile(self, filepath):
        """This function opens the given file.

        parameters
        ----------
        filepath: str
            path to the file
        """
        self.fileLoaded = True
        self.text.LoadFile(filepath)
        self.path = filepath

    def saveFile(self, path=None):
        """This function saves the current file.

        Parameters
        ----------
        path : str
            Path where the file is saved
        """
        if path is None:
            path = self.path
        try:
            self.text.SaveFile(path)
            self.GetParent().SetTitle("%s - pyed" % (self.filename))
        except TypeError:
            self.GetParent().onSaveAs(None)
            self.GetParent().SetTitle("%s - pyed" % (self.filename))

    def onClose(self, event):
        """Close the panel"""
        if self.text.IsModified():
            parent = self.GetParent()
            retval = parent.showDlg(parent, _("There are unsaved changes.\n Do you want to save"), _(
                "Unsaved Canges"), wx.YES_NO | wx.YES_DEFAULT)
            if retval == wx.ID_YES:
                self.saveFile()
        self.Destroy()

    def onModify(self, event):
        """Schows in title if text is modified."""
        if self.fileLoaded:
            self.fileLoaded = False
            return
        self.GetParent().SetTitle("*%s - pyed" % (self.filename))
        event.Skip()


class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        """Class for the MainFrame.

        The MainFrame takes the same arguments as the wx.Frame class.
        """
        super(MainFrame, self).__init__(*args, **kwargs)
        # stuff
        self.newFileCounter = 1
        filename = _("Untitled %d" % (self.newFileCounter))

        self.SetTitle("%s - pyed" % (filename))

        # widgets
        self.CreateStatusBar()
        self.writePanel = WritePanel(filename, self)

        # create menu
        filemenu = wx.Menu()
        helpmenu = wx.Menu()

        menuNew = filemenu.Append(wx.ID_NEW, _("New"), _(" Create new file"))
        menuOpen = filemenu.Append(wx.ID_OPEN, _("Open"), _(" Open file"))
        filemenu.AppendSeparator()
        menuSave = filemenu.Append(wx.ID_SAVE, _("Save", _(" Save file")))
        menuSaveAs = filemenu.Append(
            wx.ID_SAVEAS, _("Save As", _(" Save file as")))
        menuExit = filemenu.Append(wx.ID_EXIT, _("Exit"), _(" Exit Program"))
        filemenu.AppendSeparator()
        menuAbout = helpmenu.Append(wx.ID_ABOUT,
                                    _("About"), _(" Infos about this program"))

        # create menubar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, _("&File"))
        menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(menubar)

        # Eventhandler
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.onOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.newFile, menuNew)
        self.Bind(wx.EVT_MENU, self.onSave, menuSave)
        self.Bind(wx.EVT_MENU, self.onSaveAs, menuSaveAs)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        # layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.writePanel, 1, wx.EXPAND, 1)
        self.SetSizer(sizer)

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
        info.AddDeveloper("Jens Wilberg")
        info.AddDocWriter("Jens Wilberg")
        info.AddTranslator("Jens Wilberg")
        wx.adv.AboutBox(info)

    def showDlg(self, parent, message, title, style):
        """Displays a dialog."""
        dlg = wx.MessageDialog(parent=parent, message=message,
                               caption=title, style=style)
        retval = dlg.ShowModal()
        dlg.Destroy()
        return retval

    def onOpen(self, event):
        """Open a file."""
        self.writePanel.Close()
        fdlg = wx.FileDialog(self, _("Choose file"),
                             os.getcwd(), "", "*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fdlg.ShowModal() == wx.ID_OK:
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
        fdlg = wx.FileDialog(self, _("Save As"),
                             os.getcwd(), "", "*.*", wx.FD_SAVE |
                             wx.FD_OVERWRITE_PROMPT)
        if fdlg.ShowModal() == wx.ID_OK:
            self.writePanel.saveFile(fdlg.GetPath())
        fdlg.Destroy()

    def newFile(self, event):
        """"Creates a new file."""
        self.writePanel.Close()
        self.newFileCounter += 1
        filename = _("Untitled %d" % (self.newFileCounter))
        self.writePanel = WritePanel(filename, self)
        self.SetTitle("%s - pyed" % (filename))
        self.GetSizer().Add(self.writePanel, 1, wx.EXPAND, 1)
        self.Layout()
        self.writePanel.SetFocus()


def run():
    """Run the Application."""
    app = wx.App()
    frame = MainFrame(parent=None, title="pyed",
                      size=(600, 400))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
