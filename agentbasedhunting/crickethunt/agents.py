import numpy as np
import math, random

from mesa import Agent
from mesa.space import MultiGrid
"""
agents need to have step AND advance for simultaneous activation
need one agent for cricket
    choose position randomly at start from centers of hexes, stay put
    cricket chirps every 2 sec (20 tenths) unless mouse moves,
    if mouse moves start counter over
"""


def get_mouse_heading(self,pos_1,pos_2):
    """
    Find the vector from position 1 to position 2
    """
    one = np.array(pos_1)
    two = np.array(pos_2)
    heading = two - one
    if np.all([heading] == np.array([0,0])):
        # if the animal didn't move, see if the agent moves its head
        if self.random.randint(1,100) < 100*self.Pscan:
            pos_2 = np.array([pos_1[0]+self.random.randint(-1,1), pos_1[1]+self.random.randint(-1,1)])
            two = np.array(pos_2)
            heading = two - one
    if heading[0]==0:
        angular_heading=0
    else:
        angular_heading = (np.arctan(heading[1]/heading[0]))*(180/(2*math.pi))
    return angular_heading

def get_distance(pt1,pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx ** 2 + dy ** 2)

class CricketAgent(Agent):
    def __init__(self, pos, model, chirp=0):
        super().__init__(pos, model)
        self.countdown = chirp
        self.chirp = chirp
        self.pos = pos
        self.value=0

    def step(self):
        if self.countdown > self.model.cricket_delay:
            self.chirp = 1
            self.countdown=0
        else:
            self.chirp=0

    def advance(self):
        neighbors = [i for i in self.model.grid.get_neighborhood(
            self.pos, True, False, radius = self.model.cricket_range) if len(self.model.grid.get_cell_list_contents([i]))>1]
        mouse_cell = self.model.grid.get_cell_list_contents(neighbors)
        for agent in mouse_cell:
            if type(agent) is MouseAgent:
                if agent.speed > self.model.cricket_sensitivity:
                    self.countdown = 0
        self.countdown+=1

class SoundAgent(Agent):
    def __init__(self,pos,model,soundscape_value=0):
        super().__init__(pos,model)
        self.soundscape_value = soundscape_value

    def step(self):
        cricket = [agent for agent in cell for cell in self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False,radius=115)
                if type(agent) is CricketAgent]

        if cricket.chirp == 1:
            cricket_pos = cricket.pos
            #get my sound value
            # get distance from cricket
            d = get_distance(self.pos,cricket_pos)
            if d < 10:
                soundscape_value = self.pos
            if d < 30:
                soundscape_value = [self.pos[0]+self.random.randint(-15,15),self.pos[1]+ self.random.randint(-15,15)]
            if d < 50:
                soundscape_value = [self.pos[0]+self.random.randint(-25,25),self.pos[1]+ self.random.randint(-25,25)]
        else: soundscape_value=0

    def advance(self):
        self.soundscape_value=0 #always resets to zero


class GrassAgent(Agent):
    def __init__(self,pos,model,is_grass):
        super().__init__(pos,model)
        self.value = is_grass
    def step(self):
        0
    def advance(self):
        0

class MouseAgent(Agent):
    def __init__(
        self,
        pos,
        model,
        speed=2,
        velocity=0,
        belief = [0,0],
        range = 10,
        heading=0,
        dwell = 0.5,
        Pscan = 0.1,
        Lbias= 0.5,
        cohere= 1.0,
        value=0,
        stickiness = 0.5
    ):
        """
        Create a new mouse agent.

        Args:
            pos: Starting position
            speed: Distance to move per step (scalar)
            velocity: Direction vector
            belief: A vector pointing toward where the animal thought the
                last sound came from
            range: Radius of potential moves
            heading: numpy vector for the direction of movement
            Pdwell: Probability of waiting before moving again
            Pscan: If "moving" probability of "peeking" (changing heading)
                without moving body
            Lbias: likelihood to go L
            cohere: the relative importance of maintaining last direction

        """
        super().__init__(pos, model)
        # TODO make mouse start flexible
        # for now have the x,y locations for mouse intro points and cricket locations
        # for each initiation of the model, pick from these lists randomly
        self.pos = pos
        self.model= model
        self.value=0
        self.speed = speed
        self.velocity = velocity
        self.heading = heading
        self.belief = belief
        self.range = range
        self.Pdwell = dwell
        self.Pscan = Pscan
        self.Lbias = Lbias
        self.cohere_factor = cohere
        self.state_stickiness = stickiness

    def step(self):
        """
        Get the mouse's
            neighboring cells,
            current soundscape value,
            and previous heading.
        Compute the new vector and prepare to move.
        """
        # sound info contains the 'believed' pt where cricket is
        # if we're less than the Pdwell, dwell, else roam
        if self.speed == 0:
            # were paused, how likely are we to continue to pause?
            dwell = self.Pdwell*(1+self.state_stickiness)
        else:
            dwell=self.Pdwell
        x=random.randint(0,100)
        if  x < 100*dwell:
            self.new_pos = self.pos
            self.speed = 0
            # does the animal move at all this turn?
            # TODO weight by confidence in sound location? time since last pause?
        #elif np.all(soundinfo.soundscape_value > 0):
            # is the cricket chirping? if so don't move! then update beliefs
        #    self.new_pos = self.pos
        #    self.belief = agent.soundscape_value
        else: #let's move!
            # where do I think this cricket is?
            if self.speed == 0:
                cohere_factor = 0
            else:
                cohere_factor = self.cohere_factor
            current_belief = get_mouse_heading(self,self.pos,self.belief)
            self.velocity = (self.heading * cohere_factor) + (current_belief * (1-cohere_factor))*((2*math.pi)/180)
            # in radians
            self.speed = self.random.randint(3,self.range)

            new_x = int(self.pos[0] + (np.cos(self.velocity)*self.speed))
            new_y = int(self.pos[1] + (np.sin(self.velocity)*self.speed))

            # what are my options for moving?
            candidate_cells = [
                cell for cell in self.model.grid.get_neighborhood(
                    self.pos, True, False,
                    radius = self.speed)]
            # exclude grass
            candidate_moves = []
            for cell in candidate_cells:
                cell_info = self.model.grid.get_cell_list_contents(cell)
                for agent in cell_info:
                    if type(agent) is GrassAgent and agent.value == 0:
                        candidate_moves.append(cell)

            # find closest point in neighborhood that isn't grass
            min_dist = int(min([get_distance([new_x,new_y], pos) for pos in candidate_moves]))

            if min_dist == 0:
                self.new_pos = (new_x,new_y)
            else:
                final_candidates = [
                    pos for pos in candidate_moves if int(get_distance(self.pos, pos)) == min_dist
                ]
                self.random.shuffle(final_candidates)
                self.new_pos = final_candidates[0]

    def advance(self):
        self.heading = get_mouse_heading(self,self.pos,self.new_pos)
        # ADD if next to cricket, eat it (ends sim)
        self.model.grid.move_agent(self, self.new_pos)
