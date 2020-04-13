from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter
t = 1000

def n(tk, h):
    h.next_day()
    h.change_infected()
    tk.update()
    if h.num_immune == h.population:
        return
    tk.after(t,  n(tk, h))


    #tk.after_idle(n, tk, h)

def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=1600, height=900, bg="white")
    canvas.pack()
    houston = City(canvas, 2000, 400, "Urban", "Houston")


    n(tk, houston)







if __name__ == "__main__":
    main()
