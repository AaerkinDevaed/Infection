from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt

def main():
    houston = City(1500, 300, "Urban", "Houston")

    simulation_length = 30
    time = np.arange(0,simulation_length)

    immune = [0]
    healthy = [len(houston.people_list) - 1]
    infected = [1]
    quarantined = [0]
    icu = [0]
    dead = [0]

    for t in time[1:]:
        # Update time
        houston.next_day()
        # Change newly_infected to infected
        houston.change_infected()
        # Change totals in lists
        immune.append(int(houston.num_immune * 0.97))
        healthy.append(houston.num_healthy)
        infected.append(houston.num_infected)
        quarantined.append(houston.num_quarantined)
        icu.append(houston.num_icu)
        dead.append(int(0.03*houston.num_immune))

    print_info(dead, time, immune, infected, healthy, quarantined, icu)



def print_info(dead, time, immune, infected, healthy, quarantined, icu):
    print(dead)
    print(immune)
    print(infected)
    print(icu)
    plt.plot(time, immune, color = "green", label = "Immune")
    plt.plot(time, infected, color = "red", label = "Infected")
    plt.plot(time, healthy, color = "blue", label = "Healthy")
    plt.plot(time, quarantined, color = "yellow", label = "Quarantined")
    plt.plot(time, icu, color = "pink", label = "ICU")
    plt.plot(time, dead, color = "black", label = "Dead")
    plt.legend()
    plt.xlabel("# of Days")
    plt.ylabel("# of People")
    plt.show()

if __name__ == "__main__":
    main()
