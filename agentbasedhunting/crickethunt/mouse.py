import numpy as np

from mesa import Agent


class MouseAgent(Agent):
    def __init__(
        self,
        model,
        pos,
        speed,
        heading,
        range,
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
            velocity: Speed vector
            heading: numpy vector for the direction of movement
            range: Radius of potential moves
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
        self.range = range
        self.Pdwell = Pdwell
        self.Pscan = Pscan
        self.Lbias = Lbias
        self.cohere = cohere


    def step(self):
        """
        Get the mouse's neighbors, compute the new vector, and move accordingly.
        """

        neighbors = self.model.grid.get_neighbors(self.pos, self.vision, False)
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

##
        # Get neighborhood within vision
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vision
            )
            if not self.is_occupied(i)
        ]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max([self.get_sugar(pos).amount for pos in neighbors])
        candidates = [
            pos for pos in neighbors if self.get_sugar(pos).amount == max_sugar
        ]
        # Narrow down to the nearest ones
        min_dist = min([get_distance(self.pos, pos) for pos in candidates])
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

 #def get_neighbors(
#        self,
#        pos: Coordinate,
#        moore: bool,
#        include_center: bool = False,
#        radius: int = 1,
#    ) -> List[Coordinate]:
       """Return a list of neighbors to a certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).

        """
    #def eat(self):
    #    sound_patch = self.get_sound(self.pos)
    #    self.sound = self.sound - self.metabolism + sound_patch.amount
    #    sound_patch.amount = 0


    #def advance(self):
        #advance info
        #self.move()


class Boid(Agent):
    """
    A Boid-style flocker agent.

    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents.
        - Separation: avoiding getting too close to any other agent.
        - Alignment: try to fly in the same direction as the neighbors.

    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        model,
        pos,
        speed,
        velocity,
        vision,
        separation,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        """
        Create a new boid agent.

        Args:
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings

        """
        super().__init__(self, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match


    def cohere(self, neighbors):
        """
        Return the vector toward the center of mass of the local neighbors.
        """
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        """
        Return a vector away from any neighbors closer than separation dist.
        """
        me = self.pos
        them = (n.pos for n in neighbors)
        separation_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation:
                separation_vector -= self.model.space.get_heading(me, other)
        return separation_vector

    def match_heading(self, neighbors):
        """
        Return a vector of the neighbors' average heading.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
        return match_vector

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """

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
