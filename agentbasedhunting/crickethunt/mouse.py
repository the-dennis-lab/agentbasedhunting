import numpy as np

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
        return heading

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

        for agent in self.model.grid.get_cell_list_contents([pos]):
            if type(agent) is SoundAgent:
                soundinfo = agent.soundscape_value

        # does the animal move at all this turn?
        # TODO weight by confidence in sound location?
            # if we're less than the Pdwell, dwell
            # else roam

        if self.random.randint(0,100) < 100*self.Pdwell:
            self.new_pos = self.pos
        elif soundinfo > 0:
            # is the cricket chirping? if so don't move! then update beliefs
            self.new_pos = self.pos
            self.belief = agent.soundscape_value
        else: #let's move!
            neighbor_cells = get_neighborhood(self, pos, moore = True, include_center = False, radius = self.range)

            ############ self.new_pos

"""
BOID STEP
    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity += (
            self.cohere(neighbors) * self.cohere_factor
            + self.separate(neighbors) * self.separate_factor
            + self.match_heading(neighbors) * self.match_factor
        ) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.next_move = new_pos

        def advance(self):
        self.model.space.move_agent(self, new_pos)
class GrassPatch(Agent):
    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again


        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1

"""

    def advance(self):
        self.heading = get_mouse_heading(pos,new_pos)
        # if next to cricket, eat it (ends sim)
        self.model.grid.move_agent(self, new_pos)
