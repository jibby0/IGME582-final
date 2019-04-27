#!/usr/bin/python3
# Astroangles game logic
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


class AstroanglesGame:

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
    def reset(self):
        '''
        Resets the game
        '''

        # Checks if the game should be running
        self.game_running = True

        # Track health of the player. Might change amount later
        self.player_health = 3
        
        # Track correct answers
        self.correct_answers = 0
        self.gen_new_problem()

    def run(self):
        self.screen = pygame.display.get_surface()
        if not(self.screen):
                self.screen = pygame.display.set_mode(
                    (pygame.display.Info().current_w,
                     pygame.display.Info().current_h))
                pygame.display.set_caption(_("Astroangles"))
                gameicon = pygame.image.load("images/asteroid.png")
                pygame.display.set_icon(gameicon)
        self.background = pygame.image.load("activity/space_example.jpg")
        self.asteroid = pygame.image.load("images/asteroid.png")
        self.asteroid = pygame.transform.scale(self.asteroid, (int(round(pygame.display.Info().current_w // 3.2)), int(round(pygame.display.Info().current_h // 2.4))))
        self.cannon = pygame.image.load("images/spaceship.png")
        self.cannon = pygame.transform.scale(self.cannon, (pygame.display.Info().current_w // 8, pygame.display.Info().current_h // 6))
        self.bottom_bar = pygame.image.load("activity/bottom_bar_example.jpg")

        # Asteroids are always a distanced a little less than half the width of
        # the screen from the center
        self.asteroid_distance = (self.canvas.get_preferred_width()[1] // 2) * 4 // 5

        # Cannon is at the bottom of the screen, in the middle
        self.cannon_pos = (self.canvas.get_preferred_width()[1] // 2,
                           self.canvas.get_preferred_height()[1] - self.cannon.get_rect().height)
        # And starts straight up
        self.cannon_rotated = pygame.transform.rotate(self.cannon, 90)

        # Set up a new problem upon start
        self.gen_new_problem()

        # Set up the font library
        pygame.freetype.init()
        GAME_FONT = pygame.freetype.SysFont("DejaVuSans", 32)

        self.reset()

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
                    if self.game_running:
                        # Set the x, y postions of the mouse click
                        x, y = event.pos

                        # Check all asteroids to see if one of them was clicked on. Break if found
                        for ast in self.asteroids:
                            if ast.is_selected(pygame.mouse.get_pos()):
                                self.cannon_rotated = pygame.transform.rotate(
                                    self.cannon, ast.angle - 90)
                                if self.correct_angle == ast.angle:
                                    self.correct_answers += 1
                                else:
                                    self.player_health -= 1
                                    
                                    if self.player_health <= 0:
                                        self.game_running = False
                                
                                if self.player_health > 0:
                                    self.gen_new_problem()
                                break
                    else:
                        self.reset()

            self.screen.fill(colors.WHITE)
            self.screen.blit(self.background, (0, 0))

            # Draw a base line, indicating 0 degrees and 180 degrees
            pygame.draw.line(
                self.screen,
                colors.RED,
                (0, self.cannon_pos[1]),
                (self.canvas.get_preferred_width()[1], self.cannon_pos[1]))

            # Label 0 and 180 degrees
            GAME_FONT.render_to(
                self.screen,
                (0, self.cannon_pos[1]),
                '180 degrees',
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)
            GAME_FONT.render_to(
                self.screen,
                (self.canvas.get_preferred_width()[1]- 155, self.cannon_pos[1]),
                '0 degrees',
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

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

            degrees_text = '{} degrees'.format(self.correct_angle)
            correct_text = 'Correct: {}'.format(self.correct_answers)

            GAME_FONT.render_to(
                self.screen,
                (self.canvas.get_preferred_width()[1] // 2 - GAME_FONT.get_rect(degrees_text).width // 2,
                 self.canvas.get_preferred_height()[1]),
                degrees_text,
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

            GAME_FONT.render_to(
                self.screen,
                (0, self.canvas.get_preferred_height()[1]),
                'Health: {}'.format(self.player_health),
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

            GAME_FONT.render_to(
                self.screen,
                (self.canvas.get_preferred_width()[1] - GAME_FONT.get_rect(correct_text).width,
                 self.canvas.get_preferred_height()[1]),
                correct_text,
                fgcolor=colors.WHITE, bgcolor=colors.BLACK) 

            if not self.game_running:
                gameover_text = "Game Over!"
                restart_text = "Click to Restart"

                GAME_FONT.render_to(
                    self.screen,
                    (self.canvas.get_preferred_width()[1] // 2 - GAME_FONT.get_rect(gameover_text).width // 2,
                     self.canvas.get_preferred_height()[1] // 2 - 25),
                gameover_text,
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

                GAME_FONT.render_to(
                    self.screen,
                    (self.canvas.get_preferred_width()[1] // 2 - GAME_FONT.get_rect(restart_text).width // 2,
                     self.canvas.get_preferred_height()[1] // 2 + 25),
                restart_text,
                fgcolor=colors.WHITE, bgcolor=colors.BLACK)

            pygame.display.update()

        return False
