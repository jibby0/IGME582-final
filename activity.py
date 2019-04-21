# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import pygame
import sugargame.canvas

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.style import GRID_CELL_SIZE

from astrofractions import AstrofractionsGame

class AstrofractionsActivity(activity.Activity):
    """AstrofractionsActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the Astrofractions activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        self.game = AstrofractionsGame(self)
        self.game.canvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font])

        w = Gdk.Screen.width()
        h = Gdk.Screen.height() - 2 * GRID_CELL_SIZE

        self.game.canvas.set_size_request(w, h)

        self._notebook = Gtk.Notebook(show_tabs=False)
        self._notebook.add(self.game.canvas)

        self.set_canvas(self.game.canvas)
	Gdk.Screen.get_default().connect('size-changed', self.__configure_cb)
        self.canvas = self._notebook

        self.show_all()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        self.write_file(os.path.join(
                        activity.get_activity_root(), 'data', 'data'))
        w = Gdk.Screen.width()
        h = Gdk.Screen.height() - 2 * GRID_CELL_SIZE
        pygame.display.set_mode((w, h),
                                pygame.RESIZABLE)
        #self.read_file(os.path.join(activity.get_activity_root(), 'data', 'data'))
