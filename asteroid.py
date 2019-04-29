#!/usr/bin/python3
# Astroangles asteroid class

# Copyright (C) 2009 Simon Schampijer
# Copyright (C) 2019  Josh Bicking
# Copyright (C) 2019  Giovanni Aleman
# Copyright (C) 2019  Derek Erway

# Code:   https://github.com/jibby0/IGME582-final
# SPDX-License-Identifier: GPL-2.0-or-later

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
