import math

from mesa import Agent

# agents need to have step AND advance for simultaneous activation
# need one agent for cricket
    # choose position randomly at start from centers of hexes, stay put
    # cricket chirps every 2 sec (20 tenths) unless mouse moves,
    # if mouse moves start counter over
# another agent for sound information
    # sound information from the last chirp based on location
    # first emit from cricket
    # then evaluate where mouse WAS when cricket CHIRPED
    # make this landscape
# another agent for mouse
    # one mouse at a time, starts randomly from one of 5 positions
    # in the abscence of chirps, pauses and moves around randomly
    # with normal distribution of dwell and move times/lengths
    # uses last chirp to bias movements

def get_soundscape_value(pos_mouse,pos_cricket):
    """Use the location of mouse and cricket
    to determine localization information
    available to the mouse
    """
    x1,y1 = pos_mouse
    x2,y2 = pos_cricket
    dx = math.fabs(x1-x2)
    dy = math.fabs(y1-y2)
    distance = math.sqrt(dx ** 2 + dy ** 2)
    # from center to "far hallway" of adj hex
    # x 21 + 14*(# hex away) +1 for <
    # y 23 + 17*(# hex away) +1 for <

    if distance < 40:
        soundscape_value = 3
    elif distance < 80:
        soundscape_value = 2
    elif distance < 100:
        soundscape_value = 1
    else:
        soundscape_value = 0

    #get facing info
    #if facing = 0:
    #    soundscape_value = soundscape_value - 1
    return soundscape_value



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
    def __init__(self, pos, model, moore=False, chirp=0, soundscape_value=0):
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore
        self.chirp = chirp
        self.soundscape_value = soundscape_value

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
                self.pos, self.moore, False, radius=self.distance
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


class Cricket(Agent):
    # want cricket to chirp every 2 s as default
    # then add if the mouse has moved, wait 2s
    def __init__(self, pos, model, chirp):
        super().__init__(pos, model)
        self.amount = chirp
        self.chirp = chirp

    def step(self):
        # get mouse movement info

    def advance(self):
        # if mouse moved, reset amount
        if self.amount > 20: #tenths of seconds
            self.amount = 0
            self.chirp=1
        if self.amount <= 20:
            self.amount = self.amount + 1
            self.chirp = 0

# may want to make the neighborhood check actually happen from the cricket,
# since that's the sound source, and informs where "sugar"/sound is
# want to be able to know for any position of cricket,
# what directional information does the sound provide for the mouse?

# also need to somehow "end" when the cricket gets eaten
