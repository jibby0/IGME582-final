#!/usr/bin/python3
# Astrofractions game logic
#
# Modified from PhysicsGame of the Physics activity.

# Copyright (C) 2008  Alex Levenson and Brian Jordan
# Copyright (C) 2012  Daniel Francis
# Copyright (C) 2012-13  Walter Bender
# Copyright (C) 2013  Sai Vineet
# Copyright (C) 2012-13  Sugar Labs
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
from random import sample

from gi.repository import Gtk

import pygame
import pygame.freetype

import colors
from asteroid import Asteroid


class AstrofractionsGame:

    def __init__(self, activity):
        self.activity = activity
        self.box2d_fps = 50
        self.running = True

    # def write_file(self, path):
    #     # Saving to journal
    #     self.world.add.remove_mouseJoint()
    #     additional_data = {
    #         'trackinfo': self.trackinfo,
    #         'full_pos_list': self.full_pos_list,
    #         'tracked_bodies': self.tracked_bodies
    #     }
    #     self.world.json_save(path, additional_data, serialize=True)

    # def read_file(self, path):
    #     # Loading from journal
    #     self.opening_queue = path

    def get_asteroid_pos(self, d):
        '''
        Calculate the x and y positions for an asteroid that should be at a
        d degree angle from the laser.
        '''
        # Thinking of this like a triangle, calculate the length of the side
        # opposite the laser.
        distance_from_center = (int)(math.cos(math.radians(d))
                                     * self.asteroid_distance)
        x = (self.canvas.get_preferred_width()[1] // 2) + distance_from_center
        height_from_bottom = (int)(math.sin(math.radians(d))
                                   * self.asteroid_distance)
        y = self.canvas.get_preferred_height()[1] - height_from_bottom
        return (x, y)

    def gen_new_problem(self):
        '''
        Set up a new target angle & asteroids to choose from.
        '''
        angles = [d for d in range(15, 180, 15)]
        correct, wrong1, wrong2 = sample(angles, 3)
        self.correct_angle = correct
        self.asteroids = [Asteroid(correct, self.asteroid),
                          Asteroid(wrong1, self.asteroid),
                          Asteroid(wrong2, self.asteroid)]

    def run(self):
        self.screen = pygame.display.get_surface()
        if not(self.screen):
                self.screen = pygame.display.set_mode(
                    (pygame.display.Info().current_w,
                     pygame.display.Info().current_h))
                pygame.display.set_caption(_("Astrofractions"))
                gameicon = pygame.image.load("activity/asteroid_example.png")
                pygame.display.set_icon(gameicon)

        self.angle_to_guess = 0

        self.background = pygame.image.load("activity/space_example.jpg")
        self.asteroid = pygame.image.load("activity/asteroid_example.png")
        self.cannon = pygame.image.load("activity/cannon_example.jpg")
        self.bottom_bar = pygame.image.load("activity/bottom_bar_example.jpg")

        # Asteroids are always a distanced a little less than half the width of
        # the screen from the center
        self.asteroid_distance = (self.canvas.get_preferred_width()[1] // 2) * 4 // 5

        # Cannon is at the bottom of the screen, in the middle
        self.cannon_pos = (self.canvas.get_preferred_width()[1] // 2,
                           self.canvas.get_preferred_height()[1])
        # And starts straight up
        self.cannon_rotated = pygame.transform.rotate(self.cannon, 90)

        # Set up a new problem upon start
        self.gen_new_problem()

        # Set up the font library
        pygame.freetype.init()
        GAME_FONT = pygame.freetype.SysFont("DejaVuSans", 32)

        # Track correct answers
        self.correct_answers = 0

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

                    # Check all asteroids to see if one of them was clicked on. Break if found
                    for ast in self.asteroids:
                        if ast.is_selected(pygame.mouse.get_pos()):
                            self.angle_to_guess = ast.angle

                            self.cannon_rotated = pygame.transform.rotate(
                                self.cannon, self.angle_to_guess)
                            if self.correct_angle == self.angle_to_guess:
                                self.correct_answers += 1
                            else:
                                # TODO wrong answer event
                                pass
                            self.gen_new_problem()
                            break

            self.screen.fill(colors.WHITE)
            self.screen.blit(self.background, (0, 0))

            # For all asteroids, update the position to match then angle, draw
            # it to the screen
            for ast in self.asteroids:
                pygame.draw.line(
                    self.screen,
                    colors.GREEN,
                    self.cannon_pos,
                    (ast.rect.centerx, ast.rect.centery))
                ast.set_asteroid_pos(self.get_asteroid_pos(ast.angle))
                ast.update()
                self.screen.blit(ast.img, ast.rect)

            # EXAMPLE: rotate the cannon towards the 90 degree asteroid
            self.screen.blit(
                self.cannon_rotated,
                self.cannon.get_rect(center=self.cannon_pos))

            self.screen.blit(
                self.bottom_bar,
                self.bottom_bar.get_rect(
                    topleft=(0, self.canvas.get_preferred_height()[1])))

            GAME_FONT.render_to(
                self.screen,
                (self.canvas.get_preferred_width()[1] // 2,
                 self.canvas.get_preferred_height()[1]),
                '{} degrees'.format(self.correct_angle),
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

            GAME_FONT.render_to(
                self.screen,
                (0, self.canvas.get_preferred_height()[1]),
                'Correct: {}'.format(self.correct_answers),
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)
            pygame.display.update()

        return False
