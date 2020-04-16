from Person import Person
from city import City
import numpy as np
import random
import matplotlib
import atexit
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import tkinter
import time
from Parameters import *

city_data = {}
total_data = {"Totals" : [[],[],[],[],[],[]]}
t = 0
cities = [(10000, 1000, "Urban", "Atlanta", [0,0]), (5000, 400, "Semi-Urban", "Conyers", [3.5,3.5]), (500, 70, "Rural", "Covington", [6,0])]
fig, axs = plt.subplots(2,2)
time_list = [0]

def n(tk, city_list):
    if len(time_list) > 20:
        return
    time.sleep(t)
    next_day = time_list[-1] + 1
    for tracked_list in total_data["Totals"]:
        tracked_list.append(0)
    for city in city_list:
        city.next_day()
        city.change_infected()
        city_data[city.city_name][0].append(city.num_immune)
        city_data[city.city_name][1].append(city.num_healthy)
        city_data[city.city_name][2].append(city.num_infected)
        city_data[city.city_name][3].append(city.num_quarantined)
        city_data[city.city_name][4].append(city.num_icu)
        city_data[city.city_name][5].append(city.num_dead)
        for i, tracked_list in enumerate(total_data["Totals"]):
            tracked_list[next_day] += city_data[city.city_name][i][next_day]
    tk.update()
    time_list.append(next_day)
    for city in city_list:
        if city.num_immune == city.population:
            return
    tk.after(t,  n(tk, city_list))

def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=1920, height=1040, bg="white")
    canvas.pack()
    city_list = []
    for tracked_list in total_data["Totals"]:
        tracked_list.append(0)
    for city in cities:
        population = city[0]
        pop_density = city[1]
        city_type = city[2]
        city_name = city[3]
        city_loc = city[4]
        city = City(canvas, population, pop_density, city_type, city_name, city_loc)
        per_city_data = [[city.num_immune],[city.num_healthy],[city.num_infected],[city.num_quarantined],[city.num_icu],[city.num_dead]]
        city_data[city_name] = per_city_data
        city_list.append(city)
        canvas.create_text((city_loc[0]+city.side_length/2) * scale + shift, (city_loc[1]+city.side_length + 0.5) * scale + shift, text=city_name,
                                font=("Purisa", 45), fill="Black")
        for i, tracked_list in enumerate(total_data["Totals"]):
            tracked_list[0] += per_city_data[i][0]
    tk.update()

    n(tk, city_list)

def graph():
    for i, (city, data) in enumerate(dict(city_data, **total_data).items()):
        try:
            row = int(i / 2)
            col = i % 2
            current_graph = axs[row][col]
            current_graph.clear()
            current_graph.plot(time_list, data[0], color = "green", label = "Immune")
            current_graph.plot(time_list, data[1], color = "blue", label = "Healthy")
            current_graph.plot(time_list, data[2], color = "red", label = "Infected")
            current_graph.plot(time_list, data[3], color = "yellow", label = "Quarantined")
            current_graph.plot(time_list, data[4], color = "pink", label = "ICU")
            current_graph.plot(time_list, data[5], color = "black", label = "Dead")
            current_graph.legend()
            current_graph.set_title(city)
            current_graph.set_xlabel("# of Days")
            current_graph.set_ylabel("# of People")
        except:
            continue
    plt.tight_layout()
    plt.show()

atexit.register(graph)
if __name__ == "__main__":
    main()
