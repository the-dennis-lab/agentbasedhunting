"""
Mouse Hunting Cricket Sounds Model
================================

Made by Emily Jane Dennis in Jan 2021

Built off of sugarscape example model in mesa which
was a replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import MouseAgent, Cricket
from .schedule import RandomActivationByBreed
import numpy as np


class HuntingGrounds(Model):
    """
    HuntingGrounds
    """

    verbose = True  # Print-monitoring

    def __init__(self, height=85, width=115:
        """
        Create a new model with the given parameters.
        """

        # Set parameters
        self.height = height
        self.width = width

        self.schedule = SimultaneousActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {"MouseAgent": lambda m: m.schedule.get_breed_count(MouseAgent)}
        )

        # add cricket agent in one of the center circles
        # starting off based on hex_map made 2021_01_07
        # TODO later make this flexible?
        hexnum=6
        numyhex = hexnum-1
        xval = 33
        xincrement = 10
        yval = 8
        yincrement = 7
        cricket_chambers = tuple((xval,yval))

        for rowval in np.arange(1,2*(hexnum)):
            if rowval < 7:
                yval = yval+(yincrement*(rowval-1))
                numyhex = numyhex+1
                for num in np.arange(1,numyhex+1):
                    cricket_chambers.append((xval+xincrement,yval))
            else:
                numyhex = numyhex-1
                for num in np.arange(1,numyhex+1):
                    cricket_chambers.append((xval+xincrement,yval))
                    # TODO fix for DRY above two lines repeated

        # TODO make mouse start flexible
        mouse_chambers=[(58,2),(17,21),(17,65),(58,84),(98,65),(98,21)]
        # now have the x,y locations for mouse intro points and cricket locations
        # for each initiation of the model, pick from these lists randomly

        # Create grass patches
        hex_distribution = np.genfromtxt("crickethunt/hex_map.txt")
        for _, x, y in self.grid.coord_iter():
# STOPPED HERE
            max_sugar = hex_distribution[x, y]
            sugar = Cricket((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            ssa = MouseAgent((x, y), self, False, sugar, metabolism, vision)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_breed_count(MouseAgent)])

    def run_model(self, step_count=200):

        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_breed_count(MouseAgent),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_breed_count(MouseAgent),
            )
