# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import math
import numpy as np
from tkinter import *
speed_shift = 20
shift = 400
scale = 100
radius = 0.05
inf_prob = .8
avg_sicktime = 14
size = 4

class Person:
    def __init__(self, canvas, age, home, status, position, still_working, edge_size):
        self.canvas = canvas
        self.age = age
        self.side_length = edge_size*100
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        self.time_sick = 0
        self.shape = canvas.create_oval(self.position[0]*scale+shift, self.position[1]*scale+shift, self.position[0]*scale+size+shift, self.position[1]*scale+size+shift, fill='blue')


    def move(self, speed, work_increase_in_chance):
        if(self.status == "Quarantined"):
            return
        if(self.time_sick > 8):
            self.still_working = False

        if(self.still_working):
            direc = self.direct()

            self.position[0] = self.position[0] + speed * work_increase_in_chance * direc[0]
            self.position[1] = self.position[1] + speed * work_increase_in_chance * direc[1]
            self.canvas.move(self.shape, speed * work_increase_in_chance * direc[0] * speed_shift,
                             speed * work_increase_in_chance * direc[1] * speed_shift)


        else:
            direc = self.direct()

            self.position[0] = self.position[0] + speed * direc[0]
            self.position[1] = self.position[1] + speed * direc[1]
            self.canvas.move(self.shape, speed * direc[0] * speed_shift,
                             speed * direc[1] * speed_shift)

        if(np.abs(self.position[0] - self.home[0]) > 10):
            self.canvas.move(self.shape, self.home[0]*scale  - self.position[0] * scale,
                             0)
            self.position[0] = self.home[0]

        if(np.abs(self.position[1] - self.home[1]) > 10):
            self.canvas.move(self.shape, 0,
                             (self.home[1]*scale) - (self.position[1]*scale))
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

    def change_in_status (self, people_list, chance_know_sick, perc_obey):
        if self.status == "Healthy":
            count = 0
            pos = self.position
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
            if stay_healthy < .2:
                stay_healthy = .2
            if random.random() > stay_healthy:
                self.status = "Newly Infected"
                self.canvas.itemconfig(self.shape, fill='red')

        elif self.status == "Infected":
            self.time_sick += 1
            self.canvas.itemconfig(self.shape, fill='red')
            if random.random() < perc_obey * chance_know_sick:
                self.status = "Quarantined"
                self.position = self.home
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')
        elif self.status == "Quarantined":
            self.time_sick += 1
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')