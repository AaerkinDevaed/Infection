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
        # Method for initializing and constructing our city object

        self.dim = int(np.ceil(np.sqrt(population / 10)))          # find number of cells (dim^2) by assuming each cell has on average 10 people
        w = self.dim * self.dim;                                   # find dim^2
        self.quad = [[0 for x in range(0)] for y in range(w)]      # create array for cells, x is the person and y is the cells

        self.canvas = canvas

        # Percent of people still working (essential workers)based on city type
        self.perc_working_dict = {
            "Urban": .20,
            "Semi-Urban": .10,
            "Rural": .05
        }
        # Life Expectancy based on city-type.
        # This makes almost no difference, but more accuracy doesn't hurt.
        self.life_expectancy_dict = {
            "Urban": 79.1,
            "Semi-Urban": 76.9,
            "Rural": 76.7
        }
        # Percent of people who find out they are sick each day
        # (efficiency of testing, basically) based on city type
        self.testing_efficieny_dict = {
            "Urban": .3,
            "Semi-Urban": .2,
            "Rural": .1
        }
        # Percent of people who quarantine themselves
        # once they find out that they are sick based on city type.
        self.testing_obey_dict = {
            "Urban": .85,
            "Semi-Urban": .7,
            "Rural": .4
        }

        # Speed of nonessential worker based on city-type and infection
        # percentage level. - rural cities tend to have more movement
        if city_type == "Urban":
            self.social_distancing_policies = {
            0 : .15,
            1 : 0.15 - .08 * strength,
            2 : 0.15 - .12 * strength,
            3 : 0.15 - .13 * strength,
            4 : 0.15 - .14 * strength,
        }
        elif city_type == "Semi-Urban":
            self.social_distancing_policies = {
            0 : .20,
            1 : .20 - .09 * strength,
            2 : .20 - .15 * strength,
            3 : .20 - .18 * strength,
            4 : .20 - .19 * strength,
        }
        elif city_type == "Rural":
            self.social_distancing_policies = {
            0 : .50,
            1 : .50 - .24 * strength,
            2 : .50 - .375 * strength,
            3 : .50 - .43 * strength,
            4 : .50 - .45 * strength,
        }
        # use dicts to assign values depending on city type.
        self.perc_obey = self.testing_obey_dict[city_type]
        self.perc_working = self.perc_working_dict[city_type]
        self.life_expectancy = self.life_expectancy_dict[city_type]
        self.chance_know_sick = self.testing_efficieny_dict[city_type]

        # initialize variables based on passed in parameters
        self.city_name = city_name
        self.city_type = city_type
        self.population = population
        self.pop_density = pop_density
        self.area = float(population) / pop_density

        # Letting there be 1 market and 1 ICU per 500 people.
        self.markets = int(population / 500)
        if self.markets == 0:
            self.markets = 1
        self.icus = int(population / 500)
        if self.icus == 0:
            self.icus = 1
        self.people_list = []
        self.side_length = np.sqrt(self.area)

        # Populate our city with markets
        self.market_list = []
        for x in range(self.markets):
            # randomly pick a position in our city.
            market_position = [random() * self.side_length , random() * self.side_length ]
            # save position of the market and then put it on canvas
            self.market_list.append(market_position)
            self.canvas.create_text((market_position[0] + city_loc[0]) * scale + shift, (market_position[1] + city_loc[1]) * scale + shift,
                                    text="MARKET", font=("Purisa", 20), fill="Green")

        self.icu_list = []
        for x in range(self.icus):
            # randomly pick a position in our city.
            icu_position = [random() * self.side_length, random() * self.side_length ]
            # save position of the icu and then put it on canvas
            self.icu_list.append(icu_position)
            self.canvas.create_text((icu_position[0] + city_loc[0]) * scale + shift, (icu_position[1]+ city_loc[1]) * scale + shift, text="ICU",
                                    font=("Purisa", 20), fill="Purple")

        # Populate our city with people, houses
        current_pop = 0
        # until we have more people in our city than our population.
        # it will go over by at most 4, this is marginal with thousands of
        # people.
        while (current_pop < self.population):
            # Randomly generate x and y coordinates of homes
            x_home = random() * self.side_length
            y_home = random() * self.side_length

            # Put up to 5 people in each house based on picking from
            # a Gaussian distribution centered at 3 with standard deviation
            # of 1. We don't allow for there to be less than 1 person in a
            # house. 
            people_in_house = max(int(randomg.gauss(3, 1)) + 1, 1)
            # Add however many people we are about to create to current_pop
            # which serves as our growing population tracker.
            current_pop += people_in_house
            for p in range(people_in_house):
                # Randoma age
                age = random() * self.life_expectancy
                # set their home and starting positions
                home = [x_home, y_home]
                position = [x_home, y_home]
                # Start out as healthy
                status = "Healthy"
                # Default to not still_working (for once social
                # distancing policies are put in place) and to
                # not an icu_worker
                still_working = False
                icu_worker = False
                # Randomly assign them a local ICU
                icu = self.icu_list[int(random() * self.icus)]
                # We'll say perc_working of people age 20-60
                # still work outside of house (essential workers)
                if (20 < age < 60 and random() < self.perc_working):
                    still_working = True
                    if (random() < 0.1):
                        # 10% chance that an essential worker works at the
                        # ICU
                        icu_worker = True
                        if (random() < 0.5):
                            # make it a chance that their starting position
                            # is at the ICU
                            position = icu
                #assign them a local market randomly.
                market = self.market_list[int(random() * self.markets)]
                #generate their cell number based on their position - we simply assume that all cells put together cover the city area, so we find the proportion of position to the maximum position and then get the cell number from that
                quad_i = int((np.floor(((position[1] ) % self.side_length) / self.side_length * (
                            self.dim - 1)) * self.dim)) + int(
                    ((position[0] ) % self.side_length) / self.side_length * (self.dim - 1))

                # Create the person object using the parameters we have
                # generated
                p = Person(self.canvas, age, home, status, position, still_working, icu_worker, self.side_length,
                           market, icu, self.quad, quad_i, self.dim, city_loc)
                self.people_list.append([position, p])

                self.quad[quad_i].append(p)
                # self.canvas.itemconfig(p.shape, fill = _from_rgb(((2*quad_i**3)%255, (3*quad_i**3)%255, (5*quad_i**2)%255))) # for testing how our grid is spread

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
        while (len(set(self.patient_zeros)) != 3):  # we check len(set()) because
            # it's possible that we choose the same person
            # multiple times.
            self.patient_zeros.append(int(random() * population))
            self.patient_zeros = list(set(self.patient_zeros))  # Remove duplicates if we add one
        # Set status of patient zeros to infected, change their color to red
        for patient in self.patient_zeros:
            self.people_list[patient][1].status = "Infected"
            self.canvas.itemconfig(self.people_list[patient][1].shape, fill='red')

    def next_day(self):
        # Check how many people are infected. A value of
        # 1 corresponds to .1% of population, 2 to .2%, etc
        perc_inf_adj = int((float(self.num_infected) / self.population) / .001)

        # If more than .4% of the population is infected, full
        # social distancing policies are in place.
        if perc_inf_adj > 4:
            new_speed = self.social_distancing_policies[4]
        else:
            new_speed = self.social_distancing_policies[perc_inf_adj]
        # new_mult is the factor by which we multiply the speed of
        # essential workers so that they continue to move the same
        # amount regardless of social distancing policies in place
        new_mult = self.social_distancing_policies[0] / new_speed

        # Move all people and update our grid
        for p in self.people_list:
            p[1].move(new_speed, new_mult)
            p[1].update_quad()

        # There's a chance we change status, if status changes, update
        # counts being tracked
        for p in self.people_list:
            person = p[1]
            # we save their previous status and position to help determine
            # which counts we have to update
            before = person.status
            before_position = person.position
            person.change_in_status(self, self.people_list, self.chance_know_sick, self.perc_obey)
            if (before != person.status):
                # adjust takes care of basic status changes
                self.adjust(before, person.status, person)
            if person.status == "Quarantined" and person.position == person.local_icu and before_position != person.position:
                # this "if-statement" helps us determine if somebody
                # has been moved to the icu, as these are the only conditions
                # in which somebody has been moved to the icu.
                self.num_icu += 1
            if person.status == "Immune" and before == "Quarantined" and before_position == person.local_icu:
                # this "if-statement" helps us determine if somebody
                # has been moved out of the icu
                self.num_icu -= 1

    def adjust(self, before, after, person):
        # The set of conditions that need to occur to increase or decrease
        # our trackers.
        if (before == "Healthy"):
            self.num_healthy -= 1
        elif (before == "Quarantined"):
            self.num_infected -= 1
            self.num_quarantined -= 1
        elif before == "Infected" and after == "Immune":
            self.num_infected -= 1

        if (after == "Immune"):
            self.num_immune += 1
        elif (after == "Quarantined"):
            self.num_quarantined += 1
        # we have "Newly Infected" so that newly infected people don't infect
        # others on the same day in which they are infected. So we change
        # them to infected here after all of the infecting has been done.
        elif (after == "Newly Infected"):
            self.num_infected += 1
            person.status = "Infected"
