import math
from crickethunt.random_walk import RandomWalker
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

"""    @property
    def isCooroperating(self):
        return self.move == "C"

    def step(self):

        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=True)
        best_neighbor = max(neighbors, key=lambda a: a.score)
        self.next_move = best_neighbor.move

        if self.model.schedule_type != "Simultaneous":
            self.advance()

    def advance(self):
        self.move = self.next_move
        self.score += self.increment_score() """

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



    # may want to make the neighborhood check actually happen from the cricket,
    # since that's the sound source, and informs where "sugar"/sound is
    # want to be able to know for any position of cricket,
    # what directional information does the sound provide for the mouse?
    # also need to somehow "end" when the cricket gets eaten
