import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class Graph:
    """
    Cretas MSD grpah
    """
    def __init__(self, msd, timestep, title):
        """
        :param msd: dictionary with keys = numer of step,values = MSD. Choose msd.msdX/Y/Y or msd.msd for sum of directions
        :param timestep: duration of timestep or saving frames (if longer than timestep) in ps!
        :param title: Title of graph
        """
        self.msd = msd
        self.timestep = timestep
        self.title = title
        self.x = []
        self.y = []
        for key, value in self.msd.items():
            self.x.append(key*self.timestep)
            self.y.append(value)


    def plot(self):
        """
        Builds graps
        :return:
        """


        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)

        ax.set(xlabel='time [ps]', ylabel='MSD [A]',
               title=self.title)
        ax.grid()

        fig.savefig("MSD.png")
        plt.show()