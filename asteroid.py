#!/usr/bin/python3
# Astrofractions asteroid class

import os
import math

from gi.repository import Gtk
from gi.repository import Gdk

import pygame
from pygame.locals import MOUSEBUTTONUP
import colors

class Asteroid:
    def __init__(self, angle, asteroidImg):
        self.angle = angle
        self.position = (0, 0)
        self.img = asteroidImg
        self.rect = self.img.get_rect(center=self.position)

    def set_angle(self, angle):
        self.angle = angle

    def set_asteroid_pos(self, (x, y)):
        self.position = (x, y)

    def update(self):
        self.rect = self.img.get_rect(center=self.position)

    def is_selected(self,(mouse_x, mouse_y)):
        if self.rect.collidepoint((mouse_x, mouse_y)):
            return True
        return False
