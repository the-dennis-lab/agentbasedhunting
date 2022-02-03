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
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from .agents import MouseAgent, CricketAgent, GrassAgent
#from .schedule import SimultaneousActivationByBreed
import numpy as np


class HuntingGrounds(Model):
    """
    HuntingGrounds class
    """

    verbose = True  # Print-monitoring

    def __init__(self,
        height=85,
        width=115,
        mouse_dwell_probability=0.5,
        mouse_speed=3,
        mouse_velocity=0.5,
        mouse_range=10,
        mouse_scan_probability=0,
        mouse_coherence=0.5,
        mouse_left_bias=0.5,
        mouse_hearing_range = 100,
        mouse_perf_hearing_range = 20,
        mouse_accuracy_far = 25,
        mouse_behavior_stickiness = 0.5,
        cricket_delay=2,
        cricket_range=119,
        cricket_sensitivity=2
        ):
        """
        Create a new model with the given parameters.
        """

        # Set parameters
        self.height = height
        self.width = width
        self.mouse_dwell_probability = mouse_dwell_probability
        self.mouse_speed = mouse_speed
        self.mouse_velocity = mouse_velocity
        self.mouse_range = mouse_range
        self.mouse_scan_probability = mouse_scan_probability
        self.mouse_left_bias = mouse_left_bias
        self.mouse_hearing_range = mouse_hearing_range,
        self.mouse_perf_hearing_range = mouse_perf_hearing_range,
        self.mouse_accuracy_far = mouse_accuracy_far,
        self.mouse_behavior_stickiness = mouse_behavior_stickiness,
        self.cricket_delay = cricket_delay
        self.cricket_range = cricket_range
        self.cricket_sensitivity = cricket_sensitivity
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {"MouseAgent": lambda m: 1}
        )

        # Create grass patches
        grass_distribution = np.genfromtxt("crickethunt/hex_map.txt")
        for _, x, y in self.grid.coord_iter():
            print('x is {}'.format(x))
            print('y is {}'.format(y))
            is_grass = grass_distribution[x, y]
            grass = GrassAgent(self,(x,y),is_grass)
            self.grid.place_agent(grass, (x, y))
            #self.schedule.add(grass)

        # Create mouse:
        pos_mouse = self.random.choice([(2,58),(21,17),(65,17),(84,58),(65,98),(21,98)])
        mouse = MouseAgent(pos_mouse,self)
        self.grid.place_agent(mouse, pos_mouse)
        self.schedule.add(mouse)


        # add cricket agent in one of the center circles
        # starting off based on hex_map made 2021_01_07
        # TODO later make this flexible?
        side_length=6 #num of hexes along each side
        num_y_hex = (2*side_length)-1
        middle_x_val = 35
        x_increment = 14
        middle_y_val = 52
        y_increment = 10
        cricket_chambers = []

        rel_cols = int(side_length/2)-1
        for col_val in np.arange(-rel_cols,rel_cols):
            if col_val % 2: # if not even
                col_offset = int(x_increment/2)*(-col_val/abs(col_val))
                row_offset = int(y_increment/2)*(-col_val/abs(col_val))
            else: #if even
                col_offset = 0
                row_offset = 0

            rel_col_height = side_length - 1 - abs(col_val)

            for i in np.arange(-rel_col_height,rel_col_height):
                x_val = int(middle_x_val + (col_val*x_increment) + col_offset)
                y_val = int(middle_y_val + (col_val*y_increment) + row_offset)
                cricket_chambers.append((x_val,y_val))

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

    def run(self, n):
        """ Run the model for n steps. """
        for _ in range(n):
            self.step()
