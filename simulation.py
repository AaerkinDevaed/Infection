from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter
import time
t = 10
cities = [(10000, 1000, "Urban", "Atlanta"), (5000, 400, "Semi-Urban", "Conyers"), (500, 10, "Rural", "Covington")]

def n(tk, city_list):
    time.sleep(t)
    for city in city_list:
        city.next_day()
        city.change_infected()
    tk.update()
    for city in city_list:
        if city.num_immune == city.population:
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
        city_list.append(City(canvas, population, pop_density, city_type, city_name))
    tk.update()

    n(tk, city_list)







if __name__ == "__main__":
    main()
