# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import math
import numpy as np
from Parameters import *


class Person:
    def __init__(self, canvas, age, home, status, position, still_working, icu_worker, edge_size, local_market,
                 local_icu, quad, quad_i, dim, city_loc):
        self.dim = dim  # the dimension for the grid
        self.quad = quad  # array of grid
        self.quad_i = quad_i  # starting position in grid
        self.canvas = canvas  # tkinter canvas
        self.age = age  # the rest are self-explanatory variables
        self.side_length = edge_size
        self.home = home
        self.status = status
        self.position = position
        self.local_market = local_market
        self.local_icu = local_icu
        self.still_working = still_working  # bools of whether a person is still working and whether he works at icu
        self.icu_worker = icu_worker
        self.time_sick = 0
        self.city_loc = city_loc
        self.time_to_last_market = 0
        self.shape = canvas.create_oval((self.position[0] + city_loc[0]) * scale + shift, (self.position[1] + city_loc[1]) * scale + shift,
                                        # creating tkinter object for person
                                        (self.position[0]+ city_loc[0]) * scale + size + shift,
                                        (self.position[1]+ city_loc[1]) * scale + size + shift, fill='blue')

    def move(self, speed, work_increase_in_chance):
        if (
                self.status == "Quarantined"):  # quarantined people stay home - people who don't follow quarantine are never assigned the quarantined status
            return

        if (self.icu_worker == True):  # to simulate long shifts at icu, we rotate them between home and icu every day
            if self.position == self.local_icu:
                self.position = self.home
                self.canvas.move(self.shape, self.home[0] * scale - self.local_icu[0] * scale,
                                 # along with moving a person, we also have to move their object on screen
                                 (self.home[1] * scale) - (self.local_icu[1] * scale))
            else:
                self.position == self.local_icu
                self.canvas.move(self.shape, -1 * self.home[0] * scale + self.local_icu[0] * scale,
                                 -1 * (self.home[1] * scale) + (self.local_icu[1] * scale))
            return

        if (self.position == self.local_market):  # someone at a market goes home the next day
            self.position == self.home
            self.canvas.move(self.shape, -1 * self.local_market[0] * scale + self.home[0] * scale,
                             -1 * (self.local_market[1] * scale) + (self.home[1] * scale))

            return

        if random.random() < self.time_to_last_market / avg_markettime:  # the more time someone hasn't been to a market, the more likely he is to go, with a max possible time for not going
            self.position = self.local_market
            self.canvas.move(self.shape, *self.local_market[0] * scale - self.home[0] * scale,
                             (self.local_market[1] * scale) - (self.home[1] * scale))
            return

        if (self.time_sick > 8):
            self.still_working = False  # when symptoms start showing sick people don't go to work

        if (
                self.still_working):  # working people will go in a random direction, but more likely to head back home (gaussian distr in direc func)
            direc = self.direct()

            self.position[0] = self.position[0] + speed * work_increase_in_chance * direc[
                0]  # work incr in chance is represented as a faster speed for workers bc of how our model simulates interactions
            self.position[1] = self.position[1] + speed * work_increase_in_chance * direc[1]
            self.canvas.move(self.shape, speed * work_increase_in_chance * direc[0] * scale,
                             speed * work_increase_in_chance * direc[1] * scale)

        else:
            direc = self.direct()  # non-workers move same way as workers but slower by work_increase

            self.position[0] = self.position[0] + speed * direc[0]
            self.position[1] = self.position[1] + speed * direc[1]
            self.canvas.move(self.shape, speed * direc[0] * scale,
                             speed * direc[1] * scale)

        if (np.sqrt((self.position[0] - self.home[0]) ** 2 + (self.position[1] - self.home[
            1]) ** 2) > 0.5):  # even with direction more likely to be home, we still send people home if they stray too far
            self.canvas.move(self.shape, self.home[0] * scale - self.position[0] * scale,
                             (self.home[1] * scale) - (self.position[1] * scale))
            self.position[0] = self.home[0]
            self.position[1] = self.home[1]

    def direct(
            self):  # generating a random direction for someone to go to, with home being the peak of the random distribution of directions (gaussian)
        home_direct = [0, 0]
        home_direct[0] = self.home[0] - self.position[0]

        home_direct[1] = self.home[1] - self.position[1]
        sp = [random.gauss(home_direct[0], 1), random.gauss(home_direct[1], 1)]  # random dir with home as peak of gauss

        norm = math.sqrt(sp[0] ** 2 + sp[1] ** 2)  # normalizing vector
        sp[0] = sp[0] / (norm)
        sp[1] = sp[1] / (norm)

        return sp

    def change_in_status(self, parent, people_list, chance_know_sick,
                         perc_obey):  # checking grid cell it is on and those above, below, left and right for infected people and calculating probability of infection. If not healthy person, see their status

        if self.status == "Healthy":
            count = 0
            pos = self.position
            for p in self.quad[
                self.quad_i]:  # count infected, quarantined and hospitalized people person comes into contact with
                if p.status == "Infected":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if distance <= radius:
                        count += 1
                if p.status == "Quarantined":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if p.position == p.local_icu:

                        if distance <= radius:
                            count += 0.01
                    else:
                        if distance <= radius:
                            count += 0.1

            for p in self.quad[self.quad_i + 1 % self.dim ** 2]:  # repeat for adjacent cells
                if p.status == "Infected":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if distance <= radius:
                        count += 1
                if p.status == "Quarantined":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if p.position == p.local_icu:

                        if distance <= radius:
                            count += 0.01
                    else:
                        if distance <= radius:
                            count += 0.1
            for p in self.quad[self.quad_i - 1 % self.dim ** 2]:
                if p.status == "Infected":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if distance <= radius:
                        count += 1
                if p.status == "Quarantined":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if p.position == p.local_icu:

                        if distance <= radius:
                            count += 0.01
                    else:
                        if distance <= radius:
                            count += 0.1
            for p in self.quad[(self.quad_i + self.dim) % self.dim ** 2]:
                if p.status == "Infected":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if distance <= radius:
                        count += 1
                if p.status == "Quarantined":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if p.position == p.local_icu:

                        if distance <= radius:
                            count += 0.01
                    else:
                        if distance <= radius:
                            count += 0.1
            for p in self.quad[self.quad_i - self.dim]:
                if p.status == "Infected":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if distance <= radius:
                        count += 1
                if p.status == "Quarantined":
                    distance = math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2)
                    if p.position == p.local_icu:

                        if distance <= radius:
                            count += 0.01
                    else:
                        if distance <= radius:
                            count += 0.1

            stay_healthy = (1 - inf_prob) ** count  # find probability of staying healthy
            if stay_healthy < .2:  # the minimum chance of staying healthy is 20%, it can go no lower
                stay_healthy = .2
            if random.random() > stay_healthy:  # check whether a person gets infected
                self.status = "Newly Infected"
                self.canvas.itemconfig(self.shape, fill='red')

        elif self.status == "Infected":  # infected people have a chance to get quarantined or hospitalized (because some people refuse to be quarantined so they might never be quarantined before the ICU)
            self.time_sick += 1
            if random.random() < perc_obey * chance_know_sick:  # a portion of sick people know they're sick, and a portion of those will behave morally and self-isolate
                self.status = "Quarantined"
                self.canvas.move(self.shape, self.home[0] * scale - self.position[0] * scale,
                                 (self.home[1] * scale) - (self.position[1] * scale))
                self.position = self.home
                self.canvas.itemconfig(self.shape, fill='yellow')
            if random.random() < perc_to_icu:
                self.canvas.move(self.shape, (self.local_icu[0]) * scale - self.position[0] * scale,
                                 (self.local_icu[1] * scale) - (self.position[1] * scale))
                self.position = self.local_icu
                self.canvas.itemconfig(self.shape, fill='pink')
                self.status = "Quarantined"
            if random.random() < self.time_sick / avg_sicktime:  # eventually people recover and go home
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')
                if self.position == self.local_icu:
                    self.canvas.move(self.shape, (self.home[0]) * scale - self.position[0] * scale,
                                     (self.home[1] * scale) - (self.position[1] * scale))
                    self.position = self.home
                if random.random() < death_rate:  # some people die, so we delete their moving dot and add to number of dead and subtr from num of immune (bc at end of day they'll be counted as new immune)
                    parent.num_dead += 1
                    parent.num_immune -= 1
                    self.canvas.delete(self.shape)


        elif self.status == "Quarantined":  # some quarantined people get sent to icu, some recover
            self.time_sick += 1
            if random.random() < perc_to_icu:
                self.canvas.move(self.shape, self.local_icu[0] * scale - self.position[0] * scale,
                                 (self.local_icu[1] * scale) - (self.position[1] * scale))
                self.position = self.local_icu
                self.canvas.itemconfig(self.shape, fill='pink')

            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                if self.position == self.local_icu:
                    self.canvas.move(self.shape, self.home[0] * scale - self.position[0] * scale,
                                     (self.home[1] * scale) - (self.position[1] * scale))
                    self.position = self.home

                    if random.random() < death_rate * 2:  # hospitalized people are more likely to die
                        parent.num_dead += 1
                        parent.num_immune -= 1
                        self.canvas.delete(self.shape)
                elif random.random() < death_rate:
                    self.canvas.delete(self.shape)
                    parent.num_dead += 1
                self.canvas.itemconfig(self.shape, fill='grey')

    def update_quad(self):  # after every day we update which cell of grid person is in
        if self in self.quad[self.quad_i]:
            self.quad[self.quad_i].remove(self)

        quad_i = int(
            (np.floor((self.position[1] % self.side_length) / self.side_length * (self.dim - 1)) * self.dim)) + int(
            (self.position[0] % self.side_length) / self.side_length * (self.dim - 1))
        self.quad[quad_i].append(self)
