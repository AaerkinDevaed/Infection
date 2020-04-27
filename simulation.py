from Person import Person
from city import City
import numpy as np
import random
import matplotlib
import atexit
# Gotta put in this next line or it crashes.
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import tkinter
import sys
import time
from Parameters import *

city_data = {}
total_data = {"Totals": [[], [], [], [], [], []]}
t = 1
cities = [(1000, 1000, "Urban", "Atlanta", [0,0])]
# create figures for our 3 cities
# this would have to be changed depending on city count
fig, axs = plt.subplots(2,2)
time_list = [0]


def n(tk, city_list):
    time.sleep(t)  # delay for animation, tk.after wouldn't create one
    next_day = time_list[-1] + 1
    # We append 0 so that we can add in-place later (lines 40-41).
    for tracked_list in total_data["Totals"]:
        tracked_list.append(0)
    # for each city, advance to the next day, and track all of our variables
    for city in city_list:
        city.next_day()


    tk.update()  # after we update the city we move to next frame of animation
    # This checks to see if all three cities have no infected citizens.
    # if so, we end the simulation.



    tk.after(t, n(tk, city_list))  # recursively call next frame/day


def main():
    tk = tkinter.Tk()  # create tkinter object abd canvas in it
    canvas = tkinter.Canvas(tk, width=1920, height=1040, bg="white")  # the actual window w/ graphics
    canvas.pack()  # standard tkinter call that would organize any buttons we could have, is proper to still have it
    city_list = []

    for city in cities:
        population = city[0]
        pop_density = city[1]
        city_type = city[2]
        city_name = city[3]
        city_loc = city[4]
        city = City(canvas, population, pop_density, city_type, city_name,
                    city_loc)  # pass window (canvas) to city for creating objects on it
        per_city_data = [[city.num_immune], [city.num_healthy], [city.num_infected], [city.num_quarantined],
                         [city.num_icu], [city.num_dead]]

        city_list.append(city)
        canvas.create_text((city_loc[0] + city.side_length / 2) * scale + shift,
                           (city_loc[1] + city.side_length + 0.5) * scale + shift, text=city_name,
                           font=("Purisa", 45), fill="Black")

    tk.update()  # create first frame of city

    n(tk, city_list)  # call recursive animation



if __name__ == "__main__":
    main()
