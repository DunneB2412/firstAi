# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
from pacman import agents, gamestate, search, util

import ass2
import itertools


class CornersSearchRepresentation(search.SearchRepresentation):
    def __init__(self, gstate):
        super().__init__(gstate)
        self.walls = gstate.walls
        self.start_position = gstate.pacman
        left, bottom = 1, 1
        right, top = gstate.shape - 2 * util.Vector.unit
        self.corners = frozenset([util.Vector(left, bottom),
                                  util.Vector(left, top),
                                  util.Vector(right, bottom),
                                  util.Vector(right, top)])

    @property
    def start(self):
        """
        Tuple with as first element the position, and as second element
        a tuple with one boolean per corner. This boolean is False
        if the corner has not yet been visited, True otherwise.
        Initial corner check for completeness, in case we start in a corner.
        """
        return self.start_position, self.check_corners(self.start_position, (False, False, False, False))

    def is_goal(self, state: tuple) -> bool:
        """
        Whether the given state is a goal state in this representation.
        For example super().is_goal(state.vector) or super().is_goal(state[0])

        :param state: (tuple) The state to be confirmed as goal state
        :returns: (bool) True if input state is the goal state
        """
        super().is_goal(state[0])
        return False not in state[1]

    def successors(self, state: tuple) -> list:
        """
        Finds all possible successors of a state.

        :param state: (tuple) The state for which to find successors
        :returns: (list) of all successors
        """
        successors = []
        for move in util.Move.no_stop:
            new_vector = state[0] + move.vector
            if not self.walls[new_vector]:
                new_visited = self.check_corners(new_vector, state[1])
                successor = ((new_vector, new_visited), [move], 1)
                successors.append(successor)
        return successors

    def check_corners(self, position: util.Vector, visited_corners: tuple) -> tuple:
        """
        Checks whether the current position is a corner, and then returns an updated list of visited corners.

        :param position: (pacman.util.Vector) the position to check.
        :param visited_corners: (tuple) four bools for the four corners, True if visited.

        :returns: (tuple) updated four bools for which corners have been visited.
        """
        if position in self.corners:
            return tuple(visited or position == corner for visited, corner in zip(visited_corners, self.corners))
        else:
            return visited_corners

    def pathcost(self, path: list) -> int:
        """
        Calculates the cost of a path

        :param path: (list) of moves on the path to check
        :returns: (int) the cost of the path
        """
        return search.standard_pathcost(path, self.start_position, self.walls)


# Many choices are possible here, as long as they are admissible.
# Examples include the Manhattan distance to the closest corner, fastest corner, etc.
# It is also possible to use the costs of Manhattan paths from the player through
# all remaining corners, but admissibility must be ensured.
# An often-chosen but *inadmissible* heuristic is choosing a Manhattan path greedily.
# By trying all possible corner orders, we can ensure that there is no path
# with less cost than the returned heuristic value.
def corners_heuristic(state: tuple, representation: CornersSearchRepresentation) -> int:
    """
    Calculates the heuristic to the closest unvisited corner for a given position.

    :param state: (tuple) the vector of the position in question and a tuple of bools for the visited corners.
    :param representation: (CornersSearchRepresentation) the search representation.

    :returns: (int) the heuristic value to the closest corner.
    """
    position, visited = state
    corners = [c for c, vis in zip(representation.corners, visited) if not vis]
    return min(manhattan_path_cost((position,) + corner_path) for corner_path in itertools.permutations(corners))


# Again, many choices possible, as long as they are admissible
# and not prohibitively inefficient. This heuristic is the same
# as the corners heuristic above, but for the foods closest to each corner
# rather than the corners themselves.
def dots_heuristic(state: tuple, representation: CornersSearchRepresentation) -> int:
    """
    Calculates the heuristic to the foods closest to each corner.

    :param state: (tuple) the vector of the position in question and a tuple of bools for the visited corners.
    :param representation: (CornersSearchRepresentation) the search representation.

    :returns: (int) the heuristic value to the closest corner.
    """
    if state.dots:
        left, bottom = 1, 1
        right, top = representation.walls.shape - 2 * util.Vector.unit
        corners = frozenset([util.Vector(left, bottom), util.Vector(left, top),
                             util.Vector(right, bottom), util.Vector(right, top)])

        def closest_dot(corner):
            return min(state.dots, key=lambda dot: sum(abs(dot - corner)))

        closest_to_corners = {closest_dot(corner) for corner in corners}
        return min(manhattan_path_cost((state.vector,) + corner_path) for corner_path in itertools.permutations(closest_to_corners))
    else:
        return 0


def manhattan_path_cost(path: tuple) -> int:
    """
    Manhattan cost for a path

    :param path: (tuple) the path for which to calculate a cost

    :returns: (int) the cost
    """
    position = path[0]
    cost = 0
    for next_position in path[1:]:
        cost += util.manhattan(next_position, position)
        position = next_position
    return cost


class ClosestDotSearchAgent(agents.SearchAgent):
    def prepare(self, gstate):
        self.actions = []
        pacman = gstate.pacman
        while gstate.dots:
            next_segment = self.path_to_closest_dot(gstate)
            self.actions += next_segment
            for move in next_segment:
                if move not in gstate.legal_moves_vector(gstate.agents[self.id]):
                    message = f'path_to_closest_dot returned an illegal move: {move}, {gstate}'
                    raise Exception(message)
                gstate.apply_move(self.id, move)

        print(f'[ClosestDotSearchAgent] path found with length {len(self.actions)}'
              f' and pathcost {search.standard_pathcost(self.actions, pacman, gstate.walls)}')

    @staticmethod
    def path_to_closest_dot(gstate):
        return ass2.breadthfirst(AnyDotSearchRepresentation(gstate))


class AnyDotSearchRepresentation(search.PositionSearchRepresentation):
    def __init__(self, gstate):
        super().__init__(gstate)
        self.dots = gstate.dots

    def is_goal(self, state):
        return self.dots[state.x, state.y]


class ApproximateSearchAgent(agents.SearchAgent):
    def prepare(self, gstate: gamestate.Gamestate):
        pass

    def move(self, gstate: gamestate.Gamestate):
        raise exceptions.EmptyBonusAssignmentError
