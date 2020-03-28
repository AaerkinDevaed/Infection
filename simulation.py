from Person import Person
from city import City
import numpy as np
import random
import matplotlib.pyplot as plt

def main():
    houston = City(36620, 3662)

    simulation_length = 365
    time = np.arange(0,simulation_length)

    immune = [0]
    healthy = [len(houston.people_list) - 1]
    infected = [1] 


    for t in time[1:]:
        houston.next_day
        immune.append(houston.num_immune)
        healthy.append(houston.num_healthy)
        infected.append(houston.num_infected)

    print(immune)
    print(infected)
    print(healthy)
    plt.plot(time, immune, color = "green", label = "Immune")
    plt.plot(time, infected, color = "red", label = "Infected")
    plt.plot(time, healthy, color = "blue", label = "Healthy")
    plt.legend()
    plt.xlabel("# of Days")
    plt.ylabel("# of People")
    plt.show()


if __name__ == "__main__":
    main()

