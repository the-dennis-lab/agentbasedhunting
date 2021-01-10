import numpy as np
import math

from mesa import Agent


class MouseAgent(Agent):
    def __init__(
        self,
        model,
        pos,
        speed,
        velocity,
        belief = [0,0],
        range = 30,
        heading=0,
        Pdwell = 0.5,
        Pscan = 0,
        Lbias= 0.5,
        cohere= 0.5
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
        super().__init__(self, model)
        # TODO make mouse start flexible
        # for now have the x,y locations for mouse intro points and cricket locations
        # for each initiation of the model, pick from these lists randomly
        self.pos = self.random.choice([(58,2),(17,21),(17,65),(58,84),(98,65),(98,21)])
        self.speed = speed
        self.velocity = velocity
        self.heading = heading
        self.belief = belief
        self.range = range
        self.Pdwell = Pdwell
        self.Pscan = Pscan
        self.Lbias = Lbias
        self.cohere_factor = cohere

    def get_mouse_heading(self,pos1,pos2):
        """
        Find the vector from position 1 to position 2
        """
        if np.all(heading == np.array([0,0])):
            # if the animal didn't move, see if the agent moves its head
            if self.random.randint(1,100) > 100*Pscan:
                pos_2 = np.array([pos_1[0]+self.random.randint(-1,1), pos_1[1]+self.random.randint(-1,1)])

        one = np.array(pos_1)
        two = np.array(pos_2)
        heading = two - one
        angular_heading = (np.arctan(heading[1]/heading[0]))*(180/(2*math.pi))
        return angular_heading

    def get_distance(pt1,pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx ** 2 + dy ** 2)

    def get_current_sound_info(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is SoundAgent:
                return agent

    def step(self):
        """
        Get the mouse's
            neighboring cells,
            current soundscape value,
            and previous heading.
        Compute the new vector and prepare to move.
        """
        soundinfo = get_current_sound_info(self,pos)

        # if we're less than the Pdwell, dwell, else roam
        if self.random.randint(0,100) < 100*self.Pdwell:
            self.new_pos = self.pos
            # does the animal move at all this turn?
            # TODO weight by confidence in sound location? time since last pause?
        elif soundinfo.soundscape_value > 0:
            # is the cricket chirping? if so don't move! then update beliefs
            self.new_pos = self.pos
            self.belief = agent.soundscape_value
        else: #let's move!
            # what are my options for moving? (exclude grass for now)
            candidate_moves = [
                cell
                for cell in get_neighborhood(
                    self, pos, moore = True, include_center = False,
                    radius = self.range)
                if self.value is 0]
            self.velocity = (self.heading * self.cohere_factor) + (self.belief * (1-self.cohere_factor))*((2*math.pi)/180)
            # in radians
            hypotenuse = self.random.randint(3,self.range)

            new_x = self.pos[0] + (np.cos(self.velocity)*hypotenuse)
            new_y = self.pos[1] + (np.sin(self.velocity)*hypotenuse)

            # find closest point in neighborhood that isn't grass
            min_dist = min([get_distance([new_x,new_y], pos) for pos in candidate_moves])
            final_candidates = [
                pos for pos in candidates if get_distance(self.pos, pos) == min_dist
            ]
            self.random.shuffle(final_candidates)
            self.new_pos = final_candidates[0]

    def advance(self):
        self.heading = get_mouse_heading(self.pos,self.new_pos)
        # ADD if next to cricket, eat it (ends sim)
        self.model.grid.move_agent(self, self.new_pos)
