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
            grass = GrassAgent((x, y), self, is_grass)
            self.grid.place_agent(grass, (x, y))
            self.schedule.add(grass)

################## STOPPED HERE
        # Create agent:
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            #MouseAgent(self, pos, model, chirp=0, soundscape_value=0):
            ssa = MouseAgent(self, (x, y))
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
