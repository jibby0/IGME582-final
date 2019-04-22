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
import math

from gi.repository import Gtk
from gi.repository import Gdk

import pygame
from pygame.locals import MOUSEBUTTONUP

import colors


class AstrofractionsGame:

    def __init__(self, activity):
        self.activity = activity
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

    def get_asteroid_pos(self, d):
        '''
        Calculate the x and y positions for an asteroid that should be at a
        d degree angle from the laser.
        '''
        # Thinking of this like a triangle, calculate the length of the side opposite the laser.
        distance_from_center = (int) (math.cos(math.radians(d)) * self.asteroid_distance)
        x = (self.canvas.get_preferred_width()[1] // 2) + distance_from_center
        height_from_bottom = (int) (math.sin(math.radians(d)) * self.asteroid_distance)
        y = self.canvas.get_preferred_height()[1] - height_from_bottom
        return (x,y)

    def run(self):
        self.screen = pygame.display.get_surface()
	if not(self.screen):
		self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
		pygame.display.set_caption(_("Astrofractions"))
		gameicon = pygame.image.load("activity/asteroid_example.png")
		pygame.display.set_icon(gameicon)

	background = pygame.image.load("activity/space_example.jpg")
	asteroid = pygame.image.load("activity/asteroid_example.png")

	# Asteroids are always a distanced a little less than half the width of the screen from the center
        self.asteroid_distance = (self.canvas.get_preferred_width()[1] // 2) * 4 // 5

        # Cannon is at the bottom of the screen, in the middle
        self.cannon_pos = (self.canvas.get_preferred_width()[1] // 2, self.canvas.get_preferred_height()[1])

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos
                    # TODO which asteroid did we click on?
                    #if asteroid.get_rect().collidepoint(x, y):
                    #    print('clicked on image')

            self.screen.fill(colors.WHITE)
	    self.screen.blit(background, (0,0))

            # EXAMPLE: draw lines from cannon to asteroid
            pygame.draw.line(self.screen, colors.GREEN, self.cannon_pos, self.get_asteroid_pos(30))

            # EXAMPLE: degrees for astroids at 30,90, and 145 degrees
	    self.screen.blit(asteroid, asteroid.get_rect(center=self.get_asteroid_pos(30)))
	    self.screen.blit(asteroid, asteroid.get_rect(center=self.get_asteroid_pos(90)))
	    self.screen.blit(asteroid, asteroid.get_rect(center=self.get_asteroid_pos(145)))

            pygame.display.update()

        return False
