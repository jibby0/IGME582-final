#!/usr/bin/python3
# Astrofractions game logic
#
# Modified from PhysicsGame of the Physics activity.

# Copyright (C) 2008  Alex Levenson and Brian Jordan
# Copyright (C) 2012  Daniel Francis
# Copyright (C) 2012-13  Walter Bender
# Copyright (C) 2013  Sai Vineet
# Copyright (C) 2012-13  Sugar Labs

#  This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Elements is Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>

# Wiki:   http://wiki.sugarlabs.org/go/Activities/Physics
# Code:   git://git.sugarlabs.org/physics/mainline.git

import os

from gi.repository import Gtk
from gi.repository import Gdk

import pygame
from pygame.locals import MOUSEBUTTONUP




class AstrofractionsGame:

    def __init__(self, activity):
        self.activity = activity
        # Get everything set up
        self.clock = pygame.time.Clock()
        # Create the name --> instance map for components
        self.box2d_fps = 50
        self.running = True

    #def write_file(self, path):
    #    # Saving to journal
    #    self.world.add.remove_mouseJoint()
    #    additional_data = {
    #        'trackinfo': self.trackinfo,
    #        'full_pos_list': self.full_pos_list,
    #        'tracked_bodies': self.tracked_bodies
    #    }
    #    self.world.json_save(path, additional_data, serialize=True)

    #def read_file(self, path):
    #    # Loading from journal
    #    self.opening_queue = path

    def run(self):
        self.screen = pygame.display.get_surface()
        while self.running:

            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)

                # Update & Draw World
                self.screen.fill((240, 240, 240))  # #f0f0f0, light-grey

                # Flip Display
                pygame.display.flip()

            # Stay < 30 FPS to help keep the rest of the platform responsive
            self.clock.tick(30)  # Originally 50

        return False
