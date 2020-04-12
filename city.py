import numpy as np
from numpy.random import random
from Person import Person

class City:
    def __init__(self, population, pop_density, city_type):

        # Percent of people still working based on city type
        self.perc_working_dict = {
            "Urban" : .20,
            "Semi-Urban" : .10,
            "Rural" : .05
        }
        # Life Expectancy based on city-type.
        # This makes almost no difference sorry for including.
        self.life_expectancy_dict = {
            "Urban" : 79.1,
            "Semi-Urban": 76.9,
            "Rural": 76.7
        }
        # Percent of people who know they are sick
        # (efficiency of testing, basically)
        self.testing_efficieny_dict = {
            "Urban" : .03,
            "Semi-Urban" : .02,
            "Rural" : .01
        }

        # Social Distancing Policies based on city-type and infection level
        if(city_type == "Urban"):
            self.social_distancing_policies = {
            0 : [.15, 1],
            1 : [.08, (.15/.08)],
            2 : [.03, 5],
            3 : [.02, (.15/.02)],
            4 : [.01, 15]
        }
        elif(city_type == "Semi-Urban"):
            self.social_distancing_policies = {
            0 : [.20, 1],
            1 : [.11, .2/.11],
            2 : [.05, 4],
            3 : [.02, 10],
            4 : [.01, 20]
        }
        elif(city_type == "Rural"):
            self.social_distancing_policies = {
            0 : [.50, 1],
            1 : [.26, .5/.26],
            2 : [.125, 4],
            3 : [.07, .5/.07],
            4 : [.05, 10]
        }
        self.perc_working = self.perc_working_dict[city_type]
        self.life_expectancy = self.life_expectancy_dict[city_type]
        self.chance_know_sick = self.testing_efficieny_dict[city_type]

        self.city_type = city_type
        self.population = population - population % 5
        self.pop_density = pop_density
        self.area = float(population) / pop_density
        self.homes = int(population / 5)
        self.people_list = []
        self.side_length = np.sqrt(self.area)

        # Populate our city with people and houses
        for x in range(self.homes):
            # Randomly generate x and y coordinates of homes
            x_home = random()*self.side_length
            y_home = random()*self.side_length

            # Put 5 people in each house
            for p in range(5):
                # Randoma age
                age = random() * self.life_expectancy
                # Start out as healthy
                status = "Healthy"
                # Default to not still_working (for once social
                # distancing policies are put in place)
                still_working = False
                # We'll say perc_working of people age 20-60
                # still work out of house
                if(20 < age < 60 and random() < self.perc_working):
                    still_working = True
                home = [x_home, y_home]
                position =[x_home, y_home]
                p = Person(age, home, status, position, still_working, self.side_length)
                self.people_list.append([position, p])

        # We'll say nobody starts out as immune
        self.num_immune = 0
        # Number of healthy is population - 1, since one person
        # is going to be infected
        self.num_healthy = len(self.people_list) - 1
        # Set number of infected to one
        self.num_infected = 1
        # Set number of quarantined people to 0
        self.num_quarantined = 0
        # Select the lucky patient zero randomly
        self.patient_zero = int(random() * population)
        # Set status of patient zero to infected
        self.people_list[self.patient_zero][1].status = "Infected"

    def next_day(self):
        # Check how many people are infected. A value of
        # 1 corresponds to .1% of population, 2 to .2%, etc
        perc_inf_adj = int((float(self.num_infected) / self.population) / .01)

        # If more than .4% of the population is infected, full
        # social distancing policies are in place.
        if(perc_inf_adj > 4):
            new_speed, new_mult = self.social_distancing_policies[4]
        else:
            new_speed, new_mult = self.social_distancing_policies[perc_inf_adj]

        # Move all people
        for p in self.people_list:
            p[1].move(new_speed, new_mult)

        # Chance to change status, if status changes, update
        # counts
        for p in self.people_list:
            person = p[1]
            before = person.status
            person.change_in_status(self.people_list, self.chance_know_sick)
            if(before != person.status):
                self.adjust(before, person.status)


    def change_infected(self):
        for p in self.people_list:
            person = p[1]
            if person.status == "Newly Infected":
                person.status = "Infected"
                self.num_infected += 1

    def adjust(self, before, after):
        if(before == "Healthy"):
            self.num_healthy -= 1
        elif(before == "Quarantined"):
            self.num_infected -= 1
            self.num_quarantined -= 1
        elif before == "Infected" and after == "Immune":
            self.num_infected -= 1

        if(after == "Immune"):
            self.num_immune += 1
        elif(after == "Infected"):
            self.num_infected += 1
        elif(after == "Quarantined"):
            self.num_quarantined += 1

    def print_pos(self, day):
        print("DAY {}".format(day))
        for p in self.people_list:
            person = p[1]
            print(person.position)
