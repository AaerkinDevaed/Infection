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
    def __init__(self, canvas, age, home, status, position, still_working, icu_worker, edge_size, local_market, local_icu, quad, quad_i, dim):
        self.dim = dim
        self.quad = quad
        self.quad_i = quad_i
        self.canvas = canvas
        self.age = age
        self.side_length = edge_size
        self.home = home
        self.status = status
        self.position = position
        self.local_market = local_market
        self.local_icu = local_icu
        self.still_working = still_working
        self.icu_worker = icu_worker
        self.time_sick = 0
        self.time_to_last_market = 0
        self.shape = canvas.create_oval(self.position[0] * scale + shift, self.position[1] * scale + shift,
                                        self.position[0] * scale + size + shift,
                                        self.position[1] * scale + size + shift, fill='blue')

    def move(self, speed, work_increase_in_chance):
        if(self.status == "Quarantined"):
            return

        if(self.icu_worker == True):
            if self.position == self.local_icu:
                self.positon = self.home
                self.canvas.move(self.shape, self.home[0] * scale - self.local_icu[0] * scale,
                                 (self.home[1] * scale) - (self.local_icu[1] * scale))
            else:
                self.position == self.local_icu
                self.canvas.move(self.shape, -1 * self.home[0] * scale + self.local_icu[0] * scale,
                                 -1 * (self.home[1] * scale) + (self.local_icu[1] * scale))
            return

        if(self.position == self.local_market):
            self.position == self.home
            self.canvas.move(self.shape, -1 * self.local_market[0] * scale + self.home[0] * scale,
                                 -1 * (self.local_market[1] * scale) + (self.home[1] * scale))

            return

        if random.random() < self.time_to_last_market / avg_markettime:
            self.position = self.local_market
            self.canvas.move(self.shape,  * self.local_market[0] * scale - self.home[0] * scale,
                              (self.local_market[1] * scale) - (self.home[1] * scale))
            return

        if(self.time_sick > 8):
            self.still_working = False

        if(self.still_working):
            direc = self.direct()

            self.position[0] = self.position[0] + speed * work_increase_in_chance * direc[0]
            self.position[1] = self.position[1] + speed * work_increase_in_chance * direc[1]
            self.canvas.move(self.shape, speed * work_increase_in_chance * direc[0] * scale,
                             speed * work_increase_in_chance * direc[1] * scale)

        else:
            direc = self.direct()

            self.position[0] = self.position[0] + speed * direc[0]
            self.position[1] = self.position[1] + speed * direc[1]
            self.canvas.move(self.shape, speed * direc[0] * scale,
                             speed * direc[1] * scale)

        if (np.sqrt((self.position[0] - self.home[0]) ** 2 + (self.position[1] - self.home[1]) ** 2) > 0.5):
            self.canvas.move(self.shape, self.home[0] * scale - self.position[0] * scale,
                             (self.home[1] * scale) - (self.position[1] * scale))
            self.position[0] = self.home[0]
            self.position[1] = self.home[1]

    def direct(self):
        home_direct=[0,0]
        home_direct[0] = self.home[0] - self.position[0]

        home_direct[1] = self.home[1] - self.position[1]
        sp = [random.gauss(home_direct[0], 1), random.gauss(home_direct[1],1)]

        norm = math.sqrt(sp[0]**2+sp[1]**2)
        sp[0] = sp[0] / (norm)
        sp[1] = sp[1] / (norm)

        return sp

    def change_in_status (self, parent, people_list, chance_know_sick, perc_obey):
        if self.status == "Healthy":
            count = 0
            pos = self.position
            for p in self.quad[self.quad_i]:
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

            for p in self.quad[self.quad_i+1 % self.dim ** 2]:
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
            for p in self.quad[self.quad_i-1 % self.dim ** 2]:
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
            for p in self.quad[(self.quad_i+self.dim) % self.dim ** 2]:
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
            for p in self.quad[self.quad_i-self.dim]:
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

            stay_healthy = (1 - inf_prob)**count
            if stay_healthy < .2:
                stay_healthy = .2
            if random.random() > stay_healthy:
                self.status = "Newly Infected"
                self.canvas.itemconfig(self.shape, fill='red')

        elif self.status == "Infected":
            self.time_sick += 1
            if random.random() < perc_obey * chance_know_sick:
                self.status = "Quarantined"
                self.canvas.move(self.shape, self.home[0] * scale - self.position[0] * scale,
                                 (self.home[1] * scale) - (self.position[1] * scale))
                self.position = self.home
                self.canvas.itemconfig(self.shape, fill='yellow')
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')
                if random.random() < death_rate:
                    parent.num_dead += 1
                    self.canvas.delete(self.shape)

        elif self.status == "Quarantined":
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
                self.canvas.itemconfig(self.shape, fill='grey')
                if random.random() < death_rate:
                    parent.num_dead += 1
                    self.canvas.delete(self.shape)

    def update_quad (self):
        if self in self.quad[self.quad_i]:
            self.quad[self.quad_i].remove(self)

        quad_i = int((np.floor((self.position[1] % self.side_length) / self.side_length * (self.dim - 1)) * self.dim)) + int(
            (self.position[0] % self.side_length) / self.side_length * (self.dim - 1))
        self.quad[quad_i].append(self)

