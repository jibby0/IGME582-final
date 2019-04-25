#!/usr/bin/python3
# Astroangles asteroid class

# Copyright (C) 2009 Simon Schampijer
# Copyright (C) 2019  Josh Bicking
# Copyright (C) 2019  Giovanni Aleman
# Copyright (C) 2019  Derek Erway

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

# Code:   git://github.com/jibby0/IGME582-final.git

import math

import pygame
from pygame.locals import MOUSEBUTTONUP
import colors

class Asteroid:
    def __init__(self, angle, asteroidImg):
        self.angle = angle
        self.position = (0, 0)
        self.img = asteroidImg
        self.rect = self.img.get_rect(center=self.position)

    # Helper functions to set things and move the asteroids

    def set_angle(self, angle):
        self.angle = angle

    def set_asteroid_pos(self, (x, y)):
        self.position = (x, y)

    def update(self):
        self.rect = self.img.get_rect(center=self.position)

    # Checks if a point is in the asteroid
    def is_selected(self,(mouse_x, mouse_y)):
        if self.rect.collidepoint((mouse_x, mouse_y)):
            return True
        return False
