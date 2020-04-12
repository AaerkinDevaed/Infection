# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import math
import numpy as np


radius = .05
avg_age = 40
inf_prob = .8
avg_sicktime = 14

class Person:
    def __init__(self, age, home, status, position, still_working, edge_size):
        self.age = age
        self.side_length = edge_size
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        self.time_sick = 0

    def move(self, avg_speed, work_increase_in_chance):
        if(self.status == "Quarantined"):
            return
        if(self.time_sick > 8):
            self.still_working = False

        if(self.still_working):
            direc = self.direct()

            self.position[0] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[1]

        else:
            direc = self.direct()
            self.position[0] = self.position[0] + avg_speed *  avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed *  avg_age / self.age * direc[1]

        if(self.position[0] > self.side_length or self.position[0] < 0):
            self.position[0] = self.home[0]
        if(self.position[1] > self.side_length or self.position[1] < 0):
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

    def change_in_status (self, people_list, chance_know_sick):
        if self.status == "Healthy":
            count = 0
            pos=self.position
            for i in people_list:
                if i[1].status == "Infected":
                    distance = math.sqrt((i[0][0] - pos[0])**2 + (i[0][0] - pos[1])**2)
                    if distance <= radius:
                        count += 1
                if i[1].status == "Quarantined":
                    distance = math.sqrt((i[0][0] - pos[0])**2 + (i[0][0] - pos[1])**2)
                    if distance <= radius:
                        count += 0.2

            stay_healthy = (1 - inf_prob)**count
            if random.random() > stay_healthy:
                self.status = "Newly Infected"

        elif self.status == "Infected":
            self.time_sick += 1
            if random.random() < .85 * chance_know_sick:
                self.status = "Quarantined"
                self.position = self.home
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"

        elif self.status == "Quarantined":
            self.time_sick += 1
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
