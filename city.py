import numpy as np
from numpy.random import random
import random as randomg
from Person import Person
from Parameters import *

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

class City:
    def __init__(self, canvas, population, pop_density, city_type, city_name, city_loc):

        self.dim = int(np.ceil(np.sqrt(population / 10)))
        w = self.dim * self.dim;
        self.quad = [[0 for x in range(0)] for y in range(w)]

        self.canvas = canvas
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
            "Urban" : .3,
            "Semi-Urban" : .2,
            "Rural" : .1
        }
        # Percent of people who know they are sick
        # and so quarantine themselves
        self.testing_obey_dict = {
            "Urban" : .85,
            "Semi-Urban" : .7,
            "Rural" : .4
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
        # use dicts to assign values depending on city type.
        # Probably could have used a factory constructor to make this
        # much better
        self.perc_obey = self.testing_obey_dict[city_type]
        self.perc_working = self.perc_working_dict[city_type]
        self.life_expectancy = self.life_expectancy_dict[city_type]
        self.chance_know_sick = self.testing_efficieny_dict[city_type]

        self.city_name = city_name
        self.city_type = city_type
        self.population = population - population % 5
        self.pop_density = pop_density
        self.area = float(population) / pop_density
        self.markets = int(population / 500)
        self.icus = int(population / 500)
        self.people_list = []
        self.side_length = np.sqrt(self.area)

        # Populate our city with markets
        self.market_list = []
        for x in range(self.markets):
            market_position = [random()*self.side_length + city_loc[0], random()*self.side_length + city_loc[1]]
            self.market_list.append(market_position)
            self.canvas.create_text((market_position[0]) * scale + shift, (market_position[1] ) * scale + shift, text="MARKET", font=("Purisa", 20), fill="Green")

        self.icu_list = []
        for x in range(self.icus):
            icu_position = [random()*self.side_length + city_loc[0], random()*self.side_length + city_loc[1]]
            self.icu_list.append(icu_position)
            self.canvas.create_text((icu_position[0]) * scale + shift, (icu_position[1]) * scale + shift, text="ICU", font=("Purisa", 20), fill="Purple")

        # Populate our city with people, houses
        current_pop = 0
        while(current_pop < self.population):
            # Randomly generate x and y coordinates of homes
            x_home = random()*self.side_length + city_loc[0]
            y_home = random()*self.side_length + city_loc[1]

            # Put up to 5 people in each house
            people_in_house = max(int(randomg.gauss(3,1))+1, 1)
            current_pop += people_in_house
            for p in range(people_in_house):
                # Randoma age
                age = random() * self.life_expectancy
                # Start out as healthy
                status = "Healthy"
                # Default to not still_working (for once social
                # distancing policies are put in place)
                still_working = False
                icu_worker = False
                icu = self.icu_list[int(random()*self.icus)]
                # We'll say perc_working of people age 20-60
                # still work out of house
                if(20 < age < 60 and random() < self.perc_working):
                    still_working = True
                    if (random() < 0.1):
                        icu_worker = True
                home = [x_home, y_home]
                position =[x_home, y_home]

                market = self.market_list[int(random()*self.markets)]
                quad_i = int((np.floor(((position[1] + city_loc[0])% self.side_length) / self.side_length * (self.dim - 1)) * self.dim)) + int(
                    ((position[0] + city_loc[1]) % self.side_length) / self.side_length * (self.dim-1))


                p = Person(self.canvas, age, home, status, position, still_working, icu_worker, self.side_length, market, icu, self.quad, quad_i, self.dim)
                self.people_list.append([position, p])

                self.quad[quad_i].append(p)
                #self.canvas.itemconfig(p.shape, fill = _from_rgb(((2*quad_i**3)%255, (3*quad_i**3)%255, (5*quad_i**2)%255))) # for testing how our grid is spread


        # We'll say nobody starts out as immune
        self.num_immune = 0
        # Number of healthy is population - 1, since one person
        # is going to be infected
        self.num_healthy = len(self.people_list) - 3
        # Set number of infected to one
        self.num_infected = 3
        # Set number of quarantined people to 0
        self.num_quarantined = 0
        # Set number of people in ICU to 0
        self.num_icu = 0
        # Set number of dead people to 0
        self.num_dead = 0
        self.patient_zeros = []
        # Select the lucky patient zeros randomly
        while(len(set(self.patient_zeros)) != 3): # we check len(set()) because
                                                # it's possible that we choose the same person
                                                # multiple times.
            self.patient_zeros.append(int(random()*population))
            self.patient_zeros = list(set(self.patient_zeros)) # Remove duplicates if we add one
        # Set status of patient zeros to infected, change their color to red
        for patient in self.patient_zeros:
            self.people_list[patient][1].status = "Infected"
            self.canvas.itemconfig(self.people_list[patient][1].shape, fill='red')



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
            p[1].update_quad()

        # Chance to change status, if status changes, update
        # counts
        for p in self.people_list:
            person = p[1]
            before = person.status
            before_position = person.position
            person.change_in_status(self, self.people_list, self.chance_know_sick, self.perc_obey)
            if(before != person.status):
                self.adjust(before, person.status)
            if person.status == "Quarantined" and person.position == person.local_icu:
                self.num_icu += 1
            if person.status == "Immune" and before == "Quarantined" and before_position == person.local_icu:
                self.num_icu -= 1
        self.change_infected()



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
