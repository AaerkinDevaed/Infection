from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt

def main():
    houston = City(1500, 300)

    simulation_length = 30
    time = np.arange(0,simulation_length)

    immune = [0]
    healthy = [len(houston.people_list) - 1]
    infected = [1]
    quarantined = [0]

    for t in time[1:]:
        houston.next_day()
        houston.change_infected()
        immune.append(houston.num_immune)
        healthy.append(houston.num_healthy)
        infected.append(houston.num_infected)
        quarantined.append(houston.num_quarantined)

    dead = [0]
    for i in immune[1:]:
        dead.append(0.03*i)
    for i, d in enumerate(dead):
        immune[i] - d
    print_info(dead, time, immune, infected, healthy, quarantined)



def print_info(dead, time, immune, infected, healthy, quarantined):
    print(dead)
    plt.plot(time, immune, color = "green", label = "Immune")
    plt.plot(time, infected, color = "red", label = "Infected")
    plt.plot(time, healthy, color = "blue", label = "Healthy")
    plt.plot(time, quarantined, color = "yellow", label = "Quarantined")
    plt.plot(time, dead, color = "black", label = "Dead")
    plt.legend()
    plt.xlabel("# of Days")
    plt.ylabel("# of People")
    plt.show()

if __name__ == "__main__":
    main()

