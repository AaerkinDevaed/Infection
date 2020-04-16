from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter
import time
t = 10
cities = [(10000, 1000, "Urban", "Atlanta"), (5000, 400, "Semi-Urban", "Conyers"), (500, 10, "Rural", "Covington")]
city_data = {}
total_data = {"Totals" : [[],[],[],[],[],[]]}

def n(tk, city_list):
    time.sleep(t)
    for city in city_list:
        city.next_day()
        city.change_infected()
        city_data[city.name][0].append(city.num_immune)
        city_data[city.name][1].append(city.num_healthy)
        city_data[city.name][2].append(city.num_infected)
        city_data[city.name][3].append(city.num_quarantined)
        city_data[city.name][4].append(city.num_icu)
        city_data[city.name][5].append(city.num_dead)
        for i, (name, tracked_list) in enumerate(total_data.items):
            tracked_list += city_data[city.name][i]
    tk.update()
    for city in city_list:
        if city.num_immune == city.population:
            graph()
            return
    tk.after(t,  n(tk, city_list))

def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=1920, height=1040, bg="white")
    canvas.pack()
    city_list = []
    for city in cities:
        population = city[0]
        pop_density = city[1]
        city_type = city[2]
        city_name = city[3]
        city = City(canvas, population, pop_density, city_type, city_name)
        city_list.append(city)
        per_city_data = [[city.num_immune],[city.num_healthy],[city.num_infected],[city.num_quarantined],[city.num_icu],[city.num_dead]]
        city_data[city_name] = per_city_data
    tk.update()

    n(tk, city_list)

def graph():
    for city, data in dict(city_data, **total_data):
        plt.figure()
        plt.plot()
        plt.plot(time, data[0], color = "green", label = "Immune")
        plt.plot(time, data[1], color = "blue", label = "Healthy")
        plt.plot(time, data[2], color = "red", label = "Infected")
        plt.plot(time, data[3], color = "yellow", label = "Quarantined")
        plt.plot(time, data[4], color = "pink", label = "ICU")
        plt.plot(time, data[5], color = "black", label = "Dead")
        plt.legend()
        plt.title(city)
        plt.xlabel("# of Days")
        plt.ylabel("# of People")
        plt.show()
    plt.figure()


if __name__ == "__main__":
    main()
