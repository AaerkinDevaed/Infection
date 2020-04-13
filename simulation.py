from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter
import time
t = 0

def n(tk, h):
    time.sleep(t)
    h.next_day()
    h.change_infected()
    tk.update()
    if h.num_immune == h.population:
        return
    tk.after(t,  n(tk, h))


    #tk.after_idle(n, tk, h)

def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=1920, height=1040, bg="white")
    canvas.pack()
    houston = City(canvas, 2000, 100, "Urban", "Houston")
    tk.update()

    n(tk, houston)







if __name__ == "__main__":
    main()
