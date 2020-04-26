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
t = 0
cities = [(10000, 2000, "Urban", "Atlanta", [0,0]), (5000, 1000, "Semi-Urban", "Conyers", [3.5,3.5]), (1000, 200, "Rural", [6,0])]
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
        city_data[city.city_name][0].append(city.num_immune)
        city_data[city.city_name][1].append(city.num_healthy)
        city_data[city.city_name][2].append(city.num_infected)
        city_data[city.city_name][3].append(city.num_quarantined)
        city_data[city.city_name][4].append(city.num_icu)
        city_data[city.city_name][5].append(city.num_dead)
        # add each city's individual results per list to the totals list
        # so that we can graph all results added together
        for i, tracked_list in enumerate(total_data["Totals"]):
            tracked_list[next_day] += city_data[city.city_name][i][next_day]
    tk.update()  # after we update the city we move to next frame of animation
    # This checks to see if all three cities have no infected citizens.
    # if so, we end the simulation.
    count = 0
    for city in city_list:
        if city.num_infected == 0:
            count += 1
        else:
            break
        if count == len(city_list):
            graph()
            sys.exit(0)
    time_list.append(next_day)
    tk.after(t, n(tk, city_list))  # recursively call next frame/day


def main():
    tk = tkinter.Tk()  # create tkinter object abd canvas in it
    canvas = tkinter.Canvas(tk, width=1920, height=1040, bg="white")  # the actual window w/ graphics
    canvas.pack()  # standard tkinter call that would organize any buttons we could have, is proper to still have it
    city_list = []
    # same as in line 26
    for tracked_list in total_data["Totals"]:
        tracked_list.append(0)
    # Initialize cities and city data trackers.
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
        city_data[city_name] = per_city_data
        city_list.append(city)
        canvas.create_text((city_loc[0] + city.side_length / 2) * scale + shift,
                           (city_loc[1] + city.side_length + 0.5) * scale + shift, text=city_name,
                           font=("Purisa", 45), fill="Black")
        # initialize first positions for total data trackers
        for i, tracked_list in enumerate(total_data["Totals"]):
            tracked_list[0] += per_city_data[i][0]
    tk.update()  # create first frame of city

    n(tk, city_list)  # call recursive animation


def graph():
    # We double the last element so that time matches with tracker totals
    # because it exits before adding to totals.
    for i, list_tracker in enumerate(total_data['Totals']):
        total_data['Totals'][i] = list_tracker[:-1]
    # Graph each of our data trackers
    for i, (city, data) in enumerate(dict(city_data, **total_data).items()):
        row = int(i / 2)
        col = i % 2
        current_graph = axs[row][col]
        current_graph.clear()
        current_graph.plot(time_list, data[0], color="green", label="Immune")
        current_graph.plot(time_list, data[1], color="blue", label="Healthy")
        current_graph.plot(time_list, data[2], color="red", label="Infected")
        current_graph.plot(time_list, data[3], color="yellow", label="Quarantined")
        current_graph.plot(time_list, data[4], color="pink", label="ICU")
        current_graph.plot(time_list, data[5], color="black", label="Dead")
        current_graph.legend()
        current_graph.set_title(city)
        current_graph.set_xlabel("# of Days")
        current_graph.set_ylabel("# of People")
    # tight layout helps avoid overlap between figures
    plt.tight_layout()
    plt.show()

# this causes the graphes to appear once the simulation is closed.
atexit.register(graph)
if __name__ == "__main__":
    main()
