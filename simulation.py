from Person import Person
from city import City
import numpy as np
import random
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import tkinter
import time
from Parameters import *


t = 0
cities = [(1000, 1000, "Urban", "Atlanta", [0,0]), (1000, 600, "Semi-Urban", "Conyers", [3.5,3.5]), (500, 100, "Rural", "Covington", [6,0])]


def n(tk, city_list):
    time.sleep(t)

    for city in city_list:
        city.next_day()
        city.change_infected()

    tk.update()

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
        city_loc = city[4]
        neighbors = [i for i in cities if i!=city]
        city = City(canvas, population, pop_density, city_type, city_name, city_loc)
        city_list.append(city)
        canvas.create_text((city_loc[0]+city.side_length/2) * scale + shift, (city_loc[1]+city.side_length + 0.5) * scale + shift, text=city_name,
                                font=("Purisa", 45), fill="Black")

    for city in city_list:
        neighbors = [i for i in city_list if i != city]
        city.set_neighbors(neighbors)
    tk.update()

    n(tk, city_list)



if __name__ == "__main__":
    main()
