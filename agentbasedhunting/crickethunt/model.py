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

from .agents import MouseAgent, CricketAgent, GrassAgent, SoundAgent
from .schedule import SimultaneousActivationByBreed
import numpy as np


class HuntingGrounds(Model):
    """
    HuntingGrounds
    """

    verbose = True  # Print-monitoring

    def __init__(self, height=85, width=115):
        """
        Create a new model with the given parameters.
        """

        # Set parameters
        self.height = height
        self.width = width

        self.schedule = SimultaneousActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {"MouseAgent": lambda m: 1}
        )


        # Create grass patches
        grass_distribution = np.genfromtxt("crickethunt/hex_map.txt")
        for _, x, y in self.grid.coord_iter():
            is_grass = grass_distribution[x, y]
            grass = GrassAgent(self,(x,y),is_grass)
            self.grid.place_agent(grass, (x, y))
            self.schedule.add(grass)

        # Create mouse:
        pos_mouse = self.random.choice([(2,58),(21,17),(65,17),(84,58),(65,98),(21,98)])
        mouse = MouseAgent(pos_mouse,self)
        self.grid.place_agent(mouse, pos_mouse)
        self.schedule.add(mouse)


        # add cricket agent in one of the center circles
        # starting off based on hex_map made 2021_01_07
        # TODO later make this flexible?
        hexnum=6
        numyhex = hexnum-1
        xval = 33
        xincrement = 10
        yval = 8
        yincrement = 7
        cricket_chambers = [tuple((xval,yval))]

        for rowval in np.arange(1,(2*(hexnum))):
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
        [x,y] = self.random.choice(cricket_chambers)
        print([x,y])

        # Create cricket
        cricket = CricketAgent((x, y), self)
        self.grid.place_agent(cricket, (x, y))
        self.schedule.add(cricket)


        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

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
