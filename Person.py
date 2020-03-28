# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
import numpy as np
from sklearn import preprocessing

radius = 10
avg_speed = 1
avg_age = 40
inf_prob = 0.2
avg_sicktime = 14

class Person:
    def _init_(self, age, home, status, position, still_working, time_sick):
        self.age = age
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        time_sick = 0
        
    def move(self, home, position, still_working, age):
        if(still_working):
            self.position = self.position + avg_speed * 2 * avg_age / age * self.direct(home, position)
        else:
            self.position = self.position + avg_speed * avg_age / age * self.direct(home, position)

            
    def direct(self, home, position):
        home_direct = home - position
        sp = [random.gauss(home_direct(0), 1), random.gauss(home_direct(1),1)]
        sp_norm = preprocessing.normalize(sp, norm='l2')
        return sp_norm
    
    def change_in_status (self, people_list):
        if self.status == "Healthy": 
            count = 0
            for i in people_list:
                if np.linalg.norm(people_list(0) - self.position) <= radius:
                    count += 1
                    stay_healthy = (1 - inf_prob)**count
                    if random.randrange(0,1) > stay_healthy:
                        self.status = "Infected"
        elif self.status == "Infected":
            self.time_sick += 1
            if random.randrange(0,1) < self.time_sick / avg_sicktime:
                self.status = "Immune"
            
                        
            
        
    
            
        
        