
from city import City
import numpy as np
import matplotlib.pyplot as plt

def sim(pop, dens):
    rand_city = City(pop, dens)

    simulation_length = 40
    time = np.arange(0,simulation_length)

    immune = [0]
    healthy = [len(rand_city.people_list) - 1]
    infected = [1]

    for t in time[1:]:
        rand_city.next_day()
        rand_city.change_infected()
        # houston.print_pos(t)
        immune.append(rand_city.num_immune)
        healthy.append(rand_city.num_healthy)
        infected.append(rand_city.num_infected)

    dead = [0]
    for i in immune[1:]:
        dead.append(0.03*i)
    for i, d in enumerate(dead):
        immune[i] - d

    print(dead)
    plt.plot(time, immune, color = "green", label = "Immune")
    plt.plot(time, infected, color = "red", label = "Infected")
    plt.plot(time, healthy, color = "blue", label = "Healthy")
    plt.plot(time, dead, color = "black", label = "Dead")
    plt.legend()
    plt.xlabel("# of Days")
    plt.ylabel("# of People")
    plt.show()

if __name__ == "__main__":
    sim(500,300)
