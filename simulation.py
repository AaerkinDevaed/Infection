from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter

def n(tk, h):
    h.next_day()
    tk.update()
    tk.after(0, n(tk, h))
    #tk.after_idle(n, tk, h)

def main():
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=1600, height=900, bg="white")
    canvas.pack()
    houston = City(canvas, 500, 900, "Urban", "Houston")

    n(tk, houston)
    tk.after(0, n(tk, houston))
    #while houston.num_immune != houston.population:
     #   houston.next_day()
     #   print(1)
    tk.mainloop()





   # tk.mainloop()




if __name__ == "__main__":
    main()
