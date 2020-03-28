import numpy as np
from Person import Person
import random
life_expectancy = 80
class City:
    def __init__(self, population, pop_density):
        self.population = population
        self.pop_density = pop_density
        self.area = float(population) / pop_density
        self.homes = population / 5
        if population % 5 != 0:
            self.homes += 1
        self.people_list = []
        self.side_length = np.sqrt(self.area)
        self.home_placement = np.linspace(0,self.area,self.homes)
        self.num_immune = 0
        self.num_healthy = len(self.people_list) - 1
        self.num_infected = 1
        counter = 0
        for home in self.home_placement:
            x_home = home % self.side_length
            y_home = home / self.side_length
            for p in range(5):
                if(counter > self.population):
                    break
                age = random.random() * life_expectancy
                status = "Healthy"
                still_working = False
                if(20 < age < 60 and random.random() * 100 < 20):
                    still_working = True
                home = [x_home, y_home]
                position =[x_home, y_home]
                p = Person(age, home, status, position, still_working)
                self.people_list.append([position, p])
                counter += 1

    def next_day(self):
        for p in self.people_list[1]:
            p.move()
        for p in self.people_list[1]:
            before = p.status
            p.change_in_status(self.people_list)
            if(before != p.status):
                self.adjust(before, p.status)

    def adjust(self, before, after):
        if(before == "Healthy"):
            self.num_healthy -= 1
        else:
            self.num_infected -= 1
        if(after == "Immune"):
            self.num_immune += 1
        else:
            self.num_infected += 1

