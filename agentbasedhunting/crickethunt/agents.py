import math

from mesa import Agent
"""
agents need to have step AND advance for simultaneous activation
need one agent for cricket
    choose position randomly at start from centers of hexes, stay put
    cricket chirps every 2 sec (20 tenths) unless mouse moves,
    if mouse moves start counter over
another agent for sound information
    sound information from the last chirp based on location
    first emit from cricket
    then evaluate where mouse WAS when cricket CHIRPED
    make this landscape
another agent for mouse
    one mouse at a time, starts randomly from one of 5 positions
    in the abscence of chirps, pauses and moves around randomly
    with normal distribution of dwell and move times/lengths
    later add species-specific properties
    uses last chirp to bias movements
"""

def get_angle_to_cricket(pos_mouse,pos_cricket):
    """Use the location of mouse and cricket
    to determine localization information
    available to the mouse
    """
    x1,y1 = pos_mouse
    x2,y2 = pos_cricket
    dx = math.fabs(x1-x2)
    dy = math.fabs(y1-y2)
    distance = math.sqrt(dx ** 2 + dy ** 2)
    # calculate angle to cricket
    angle = (180*np.arcsin(abs(y1-y2)/distance))/3.141592653589793
    return distance
    return angle

class SoundAgent(Agent):
    def __init__(self,pos,model,soundscape_value=0):
        super().__init__(pos,model)
        self.soundscape_value = soundscape_value

    def step(self):
        if chirp is 1:
            self.soundscape_value = get_soundscape_value(pos_mouse,pos_cricket)
        else:
            self.soundscape_value = 0

    def advance(self):
        self.soundscape_value=0 #always zero unless cricket is chirping

class MouseAgent(Agent):
    def __init__(self, pos, model, chirp=0, soundscape_value=0):
        super().__init__(pos, model)
        # TODO make mouse start flexible
        # now have the x,y locations for mouse intro points and cricket locations
        # for each initiation of the model, pick from these lists randomly
        self.pos = self.random.choice([(58,2),(17,21),(17,65),(58,84),(98,65),(98,21)])
        self.chirp = chirp
        self.soundscape_value = soundscape_value

    # want to take the angle and add weight animal direction based
    # on the angle. Depending on the distance, there should be some
    # uncertainty. This could be implemented many ways, one of which
    # is to add a random angle from as rand(0,10)*(1 or 2 or...)
    # to the correct one.
    def get_direction(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is SoundAgent:
                return agent #this used to be checking for sugar

    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return len(this_cell) > 1

    def move(self):
        # Get neighborhood within travel distance
        # first generate travel distance
        random.randint(5,25)
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, False, radius=self.distance
            )
            if not self.is_occupied(i)
        ]
        neighbors.append(self.pos)
        # STOPPEDHERE
        # want to change this to find all empty cells and
        # 1. move randomly in a single direction until a junction
        # 2. if there's sound info move toward belief
        # 3. sometimes don't move
        # was from ants 'looking' for most sugar
        dir_belief = max([self.get_sound(pos).amount for pos in neighbors])
        candidates = [
            pos for pos in neighbors if self.get_sound(pos).amount == dir_belief
        ]
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    #def eat(self):
    #    sound_patch = self.get_sound(self.pos)
    #    self.sound = self.sound - self.metabolism + sound_patch.amount
    #    sound_patch.amount = 0

    def step(self):
        self.move()

    def advance(self):
        #advance info
        self.move()


class CricketAgent(Agent):
    def __init__(self, pos, model, chirp=0):
        super().__init__(pos, model)
        self.amount = chirp
        self.chirp = chirp
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
        self.pos =


    # want cricket to chirp every 2 s as default
    # then add if the mouse has moved, wait 2s

    def step(self):
        # get mouse movement info
        self.chirp=0
    def advance(self):
        # if mouse moved, reset amount
        if self.amount > 20: #tenths of seconds
            self.amount = 0
            self.chirp=1
        if self.amount <= 20:
            self.amount = self.amount + 1
            self.chirp = 0

        #self.pos = pos
        #self.score = 0
        #if starting_move:
        #     self.move = starting_move
        #else:
        #    self.move = self.random.choice(["C", "D"])
        #self.next_move = None

    @property
    def isCooroperating(self):
        return self.move == "C"

    def step(self):
        """ Get the neighbors' moves, and change own move accordingly. """
        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=True)
        best_neighbor = max(neighbors, key=lambda a: a.score)
        self.next_move = best_neighbor.move

        if self.model.schedule_type != "Simultaneous":
            self.advance()

    def advance(self):
        self.move = self.next_move
        self.score += self.increment_score()


    # may want to make the neighborhood check actually happen from the cricket,
    # since that's the sound source, and informs where "sugar"/sound is
    # want to be able to know for any position of cricket,
    # what directional information does the sound provide for the mouse?
    # also need to somehow "end" when the cricket gets eaten
