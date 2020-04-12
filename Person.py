# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import math
import numpy as np
from tkinter import *
<<<<<<< Updated upstream
import time
=======
>>>>>>> Stashed changes

radius = .05
avg_speed = .01
avg_age = 40
inf_prob = .8
avg_sicktime = 14
work_increase_in_chance = 15

class Person:
    def __init__(self, canvas, age, home, status, position, still_working, edge_size):
        self.age = age
        self.side_length = edge_size
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        self.time_sick = 0
        self.canvas = canvas
        if status == "Infected":
<<<<<<< Updated upstream
            self.shape = canvas.create_oval(self.position[0]*10, self.position[1]*10, 100, 100, fill='red') #self.position[1]*10+800
        if status == "Healthy":
            self.shape = canvas.create_oval(self.position[0]*10, self.position[1]*10, 1, 1, fill='blue')
        if status == "Immune":
            self.shape = canvas.create_oval(self.position[0]*10, self.position[1]*10, 5, 5, fill='grey')
=======
            self.shape = canvas.create_oval(self.position[0], self.position[1], self.position[0] + 2,
                                            self.position[1] + 2, fill='red')  # self.position[1]*10+800
            self.canvas.itemconfig(self.shape, fill=active)
        if status == "Healthy":
            self.shape = canvas.create_oval(self.position[0], self.position[1], self.position[0] + 2,
                                            self.position[1] + 2, fill='blue')
        if status == "Immune":
            self.shape = canvas.create_oval(self.position[0], self.position[1], self.position[0] + 2,
                                            self.position[1] + 2, fill='grey')
>>>>>>> Stashed changes

    def move(self):
        if(self.still_working):
            direc = self.direct()

            self.position[0] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[1]
<<<<<<< Updated upstream
            self.canvas.move(self.shape, avg_speed * work_increase_in_chance * avg_age * 10 / self.age * direc[0], avg_speed * work_increase_in_chance * avg_age / self.age * direc[1])
=======
            self.canvas.move(self.shape, avg_speed * work_increase_in_chance * avg_age * 10 / self.age * direc[0],
                             avg_speed * work_increase_in_chance * avg_age / self.age * direc[1])

>>>>>>> Stashed changes

        else:
            direc = self.direct()
            self.position[0] = self.position[0] + avg_speed *  avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed *  avg_age / self.age * direc[1]
<<<<<<< Updated upstream
            self.canvas.move(self.shape, avg_speed * avg_age * 10 / self.age * direc[0], avg_speed * work_increase_in_chance * avg_age / self.age * direc[1])
=======
            self.canvas.move(self.shape, avg_speed * avg_age * 10 / self.age * direc[0],
                             avg_speed * work_increase_in_chance * avg_age / self.age * direc[1])
>>>>>>> Stashed changes

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

    def change_in_status (self, people_list):
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
<<<<<<< Updated upstream
        elif self.status == "Infected":
            self.time_sick += 1
=======
                self.canvas.itemconfig(self.shape, fill='red')
        elif self.status == "Infected":
            self.time_sick += 1
            if random.random() < .85 * chance_know_sick:
                self.status = "Quarantined"
                self.canvas.itemconfig(self.shape, fill='yellow')
                self.position = self.home
>>>>>>> Stashed changes
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')
        elif self.status == "Quarantined":
            self.time_sick += 1
            if random.random() < self.time_sick / avg_sicktime:
                self.status = "Immune"
                self.canvas.itemconfig(self.shape, fill='grey')