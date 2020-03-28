from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt

def main():
    houston = City(36620, 3662)

    simulation_length = 365
    time = np.arange(1,simulation_length + 1)

    immune = [0]
    healthy = [len(houston.people_list) - 1]
    infected = [1] 


    for t in time:
        houston.next_day
        immune.append(houston.num_immune)
        healthy.append(houston.num_healthy)
        infected.append(houston.num_infected)
    plt.plot(t, immune, color = "green")
    plt.plot(t, infected, color = "red")
    plt.plot(t, healthy, color = "blue")

