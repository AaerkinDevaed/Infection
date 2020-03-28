# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Daniil Huryn)s
"""
import random
from sklearn import preprocessing

avg_speed = 1
avg_age = 40


class Person:
    def _init_(self, age, home, status, position, still_working):
        self.age = age
        self.home = home
        self.status = status
        self.position = position
        self.still_working = still_working
        
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
        
    
            
        
        