# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import math
import numpy as np


radius = 10
avg_speed = 1
avg_age = 40
inf_prob = 0.2
avg_sicktime = 14
work_increase_in_chance = 2

class Person:
    def __init__(self, age, home, status, position, still_working):
        self.age = age
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        self.time_sick = 0
        
    def move(self):
        
        if(self.still_working):
            direc = self.direct()
            
            self.position[0] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed * work_increase_in_chance * avg_age / self.age * direc[1]
            
        else:
            direc = self.direct()
            self.position[0] = self.position[0] + avg_speed *  avg_age / self.age * direc[0]
            self.position[1] = self.position[0] + avg_speed *  avg_age / self.age * direc[1]
        
            
    def direct(self):
        home_direct=[0,0]
        home_direct[0] = self.home[0] - self.position[0]
        
        home_direct[1] = self.home[1] - self.position[1]
        sp = [random.gauss(home_direct[0], 1), random.gauss(home_direct[1],1)]
        
        norm = math.sqrt(sp[0]**2+sp[1]**2)
        sp[0] = sp[0] / (norm)
        sp[0] = sp[1] / (norm)
        
        return sp
    
    def change_in_status (self, people_list):
        if self.status == "Healthy": 
            count = 0
            for i in people_list: 
                pos=self.position
                if math.sqrt((i[0][0] - pos[0])**2 + (i[0][0] - pos[1])**2) <= radius:
                    count += 1
                    stay_healthy = (1 - inf_prob)**count
                    if random.randrange(0,1) > stay_healthy:
                        self.status = "Infected"
        elif self.status == "Infected":
            self.time_sick += 1
            if random.randrange(0,1) < self.time_sick / avg_sicktime:
                self.status = "Immune"
            
Person(1, (1,1), "Healthy", (1,1), 0)                       
            
        
    
            
        
        