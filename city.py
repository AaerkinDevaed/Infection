import numpy as np
from Person import Person
import random
life_expectancy = 80
class City:
    def __init__(self, population, pop_density):
        self.population = population
        self.pop_density = pop_density
        self.area = pop_density / float(population)
        self.homes = population / 5
        if population % 5 != 0:
            self.homes += 1
        self.people_list = []
        self.side_length = np.sqrt(self.area)
        self.home_placement = np.linspace(0,self.area,self.homes)
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

Houston = City(4000, 40)
print(Houston.people_list)

