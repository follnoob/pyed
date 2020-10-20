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
"""Implementation of dialogs."""
import wx

_ = wx.GetTranslation


class GotoDialog(wx.Dialog):
    """Class for goto dialog.

    This class uses the same parameters as wx.Dialog.

    Parameters
    ----------
    parent : wx.Window
        parent window
    id : int
        id of the dialog
    max : tuple of int
        max value for line and column
    title : str
        title of the dialog
    """

    def __init__(self, parent, id=wx.ID_ANY, max=(1, 0), title=_("GoTo"), *args,
                 **kwargs):
        """init."""
        super(wx.Dialog, self).__init__(parent, id, title, *args, **kwargs)
        self._ok = False
        # Items
        self.spinLine = wx.SpinCtrl(
            self, wx.ID_ANY, min=1, max=max[0], initial=1)
        spinLineLabel = wx.StaticText(self, wx.ID_ANY, _("Line: "))
        self.spinColumn = wx.SpinCtrl(self, wx.ID_ANY, max=max[1], initial=0)
        spinColumnLabel = wx.StaticText(self, wx.ID_ANY, _("Column: "))
        okButton = wx.Button(self, wx.ID_OK, _("Jump To"))
        cancelButton = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        okButton.Bind(wx.EVT_BUTTON, self.onOK)
        self.Bind(wx.EVT_SPINCTRL, self.onSpin, self.spinLine)

        # Layout
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.SetAffirmativeButton(okButton)
        btnSizer.SetCancelButton(cancelButton)
        btnSizer.Realize()

        lineSize = wx.BoxSizer(wx.HORIZONTAL)
        lineSize.Add(spinLineLabel, 1, wx.EXPAND, 1)
        lineSize.Add(self.spinLine, 1, wx.EXPAND, 1)

        columnSizer = wx.BoxSizer(wx.HORIZONTAL)
        columnSizer.Add(spinColumnLabel, 1, wx.EXPAND, 0)
        columnSizer.Add(self.spinColumn, 1, wx.EXPAND, 1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(lineSize)
        mainSizer.AddSpacer(10)
        mainSizer.Add(columnSizer)
        mainSizer.AddSpacer(10)
        mainSizer.Add(btnSizer, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(mainSizer)

    def onOK(self, event):
        """Handles buttonclicks."""
        self._ok = True
        event.Skip()

    def onSpin(self, event):
        """Handles spincontrol events."""
        n = self.spinLine.GetValue() - 1
        columns = len(self.GetParent().text.GetLineText(n))
        self.spinColumn.SetMax(columns)

    def GetValue(self):
        """Returns line and column.

        This function returns the line and column if the user selected them.
        otherwise it returns None.

        Returns
        -------
        tuple of int or None
            (line, column)
        """
        if not self._ok:
            return None

        return (self.spinLine.GetValue() - 1, self.spinColumn.GetValue())
