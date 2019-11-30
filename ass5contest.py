# enter your names and student numbers below
# brian (s1016603)
# rebecca (s1019789)


# -n 10 -l contestLevel0_3 contest
# -n 10 -l contestLevel1_2 contest
# -n 10 -l contestLevel2_3 contest
# -n 10 -l contestLevel3_4 contest
# -n 10 -l trickyClassic contest
# -l trickySearch contest    562
# -l bigMaze -d no contest         374
# -n 10 -d no contest    2600 , 2720

from pacman import agents, gamestate, util, distancer, search
import ass2


class ContestAgent(agents.PacmanAgent):
    """
    The code below specifies a totally moronic ContestAgent.
    It just moves to the neighbouring cell with the highest game score.
    It does not look ahead and does not even try to avoid ghosts.
    You can do far better!
    """
    distance_map = None
    corner_check = False  # use EscapeRepresentation to see if packman can escape positions
    # set to false because of the fact it dramaticly adds time to difficult desitions

    def prepare(self, gstate):
        """
        Use this method for initializing tour ContestAgent.
        The provided stump only calls the prepare of the mother class.
        You might want to add other things, for instance
        calling the precompute_distances() method of the Distancer class
        """
        self.distance_map = distancer.Distancer(gstate)
        self.distance_map.precompute_distances()
        super().prepare(gstate)

    def move(self, gstate: gamestate.Gamestate):
        """
        called by agent to find an 'appropiate' move
        :param gstate:
        :return: 'best' move
        """
        candidates = []  # refresh candidates
        moves = gstate.legal_moves_vector(gstate.pacman)  # get legal moves
        for move in moves:  # turns moves into candidates
            candidate = [move, 0, []]  # a candidate is a tuple of a move, value and goals it gows towards
            candidates.append(candidate)

        # adjusts candidates with weights from targeted moves
        self.targeted_moves(candidates, gstate)  # goal component
        for i in range(len(candidates)):  # evaluates the move further to see if it is realy good or not
            candidates[i][1] += self.new_better_evaluate(gstate, tuple(candidates[i]))  # reflex component

        best = candidates[0]  # finds the best evaluated candidate
        for candidate in candidates:
            if candidate[1] > best[1]:
                best = candidate

        return best[0]  # extracts the move from the candidate

    def new_better_evaluate(self, gstate: gamestate.Gamestate, candidate: tuple):
        """
        evaluates a gamestate according to successor_dots and ghosts
        :param gstate: game state
        :param candidate: move candidate: tuple of move, score and targets
        :return:
        """
        move, score, targets = candidate
        successor = gstate.successor(gstate.PACMAN_ID, move)  # create successor to evaluate

        if successor.loss:  # if lose don't go
            return float('-inf')
        if successor.win:  # if win go go go
            return float('inf')

        score = (successor.score-gstate.score+1) * 10  # base value is the difference beteen parent gstate and successor

        if "pelit" not in targets and self.corner_check:  # if conor check should be exucuted
            if self.is_cornered(successor):
                score += -110  # if this moov corners packman then it's a dangerous move
                if move == util.Move.stop:
                    return float('-inf')  # don't sit and wait to die

        eatable_ghosts, ghosts, dump, dump = self.rechable_goals(successor)
        successor_dots = successor.dots.list()
        pelits = successor.pellets.list()

        """
        finds ahe closest vector from target and its distance
        and the distance of all other elemets in targets combined
        """
        dot_cost, dot, dots_cost = find_closest(successor.pacman, successor_dots, self.distance_map)
        pelit_cost, dump, dump = find_closest(successor.pacman, pelits, self.distance_map)
        # find extract ghost distances
        ghost_distance, dump, dump = find_closest(successor.pacman, ghosts, self.distance_map)
        eatable_distance, dump, dump = find_closest(successor.pacman, eatable_ghosts, self.distance_map)

        # calculates how the ghost's presance affects the value of the state
        ghost_initative: float = 0
        if len(ghosts) > 0:
            # ghost initative stands moast when ghosts are closer than 3
            ghost_initative += -(10 ** (3 / (ghost_distance + 0.1))) + ghost_distance/10
        if len(eatable_ghosts) > 0:
            ghost_initative += - (eatable_distance * 1.5)*50

        # calculates how the successor's_dots affects the value of the state
        dot_initative = -dot_cost
        dot_initative += (len(gstate.dots.list()) - len(successor.dots.list())) * 50
        dot_initative += - (dots_cost / (len(successor_dots)/2))

        # canculate pelit inititive
        pelit_inititive = 0
        if len(pelits) > 0:
            pelit_inititive += -(pelit_cost * 2)
        pelit_inititive += (len(gstate.pellets.list()) - len(successor.pellets.list())) * 75
        # always show the difference (works for last dot)


        return score + dot_initative*2 + ghost_initative*2 + pelit_inititive*4

    def is_cornered(self, gstate: gamestate.Gamestate):
        """
        rins the escape representation for a packman
        :param gstate:
        :return: if packman is likely trapped
        """
        scary = []
        for i, ghost in enumerate(gstate.ghosts):
            if gstate.timers[i] == 0:
                scary.append(ghost)
        representation = EscapeRepresentation(gstate, gstate.pacman, scary, self.distance_map)
        escape_path = ass2.astar(representation, heuristic)
        return escape_path is None

    def targeted_moves(self, candidates, gstate: gamestate.Gamestate):
        """
        updates existing with moves that gows towards targets returned by reachable goals
        :param candidates: list of moves and their values based on goals
        :param gstate:
        :return: updated existing list
        """
        eatable_ghosts, scary_ghosts, pelits, target_dots = self.rechable_goals(gstate)
        dots = gstate.dots.list()

        no_go_vectors = self.scary_vectors(scary_ghosts, gstate)

        # deside on weights and dubble them if they need to be cleaned up
        ghost_weight = 100
        if len(eatable_ghosts) > len(dots)/4:
            no_go_vectors += dots
            ghost_weight = ghost_weight * 2
        pelit_weight = 120
        if len(pelits) > len(dots)/4:
            no_go_vectors += dots
            pelit_weight = pelit_weight * 2
        dot_weigth = 20

        if len(eatable_ghosts) > 0:
            no_go_vectors += gstate.pellets.list()  # try not to get pelits if there is ghosts to find
            info = (ghost_weight, "dot")  # look for a pelit
            candidates = self.get_move(candidates, gstate, eatable_ghosts, no_go_vectors, scary_ghosts, info, False)

        if len(pelits) > 0:
            info = (pelit_weight, "pelit")  # look for a pelit
            candidates = self.get_move(candidates, gstate, pelits, no_go_vectors, scary_ghosts, info, True)

        # always find for dots
        info = (dot_weigth, "dot")  # look for a dot
        candidates = self.get_move(candidates, gstate, target_dots, no_go_vectors, scary_ghosts,
                                   info, len(target_dots) == 1)

        return candidates

    def rechable_goals(self, gstate: gamestate.Gamestate):
        """
        finds reachable goals
        :param gstate:
        :return: a list of lists of moves that lead to a goal
        """
        chasable_ghosts = []
        scary_ghosts = []
        scared_ghosts = []
        for I, ghost in enumerate(gstate.ghosts):
            dis = self.distance_map.get_distance(gstate.pacman, ghost)
            not_spawn_point = self.distance_map.get_distance(ghost, gstate.starts[I+1]) > 3  # +1 because of packman
            if gstate.timers[I] > dis:  # chasable eatable ghosts
                scared_ghosts.append(ghost)
                if not_spawn_point:  # if the ghost wont respawn on packman if he eats it
                    chasable_ghosts.append(ghost)  # add good targets
            else:
                scary_ghosts.append(ghost)  # add to scary ghosts list

        pelits = []
        if len(scared_ghosts) == 0 or (len(gstate.pellets.list()) >= len(gstate.dots.list())):
            for I, pelit in enumerate(gstate.pellets.list()):
                dis = self.distance_map.get_distance(gstate.pacman, pelit)
                if dis < 10:  # chasable eatable ghosts
                    pelits.append(pelit)

        dots = []
        for I, dot in enumerate(gstate.dots.list()):
                dis = self.distance_map.get_distance(gstate.pacman, dot)
                if dis < 20:  # chasable eatable ghosts
                    dots.append(dot)
        return chasable_ghosts, scary_ghosts, pelits, dots

    def get_move(self, candidates, gstate, goals, no_go, scary_ghosts, goal_info: tuple, safe_if_reached: bool):
        """
        finds most optimal move and the distance to the goal
        :param candidates: list of moves and their values based on goals
        :param gstate: current gamestate
        :param goals: targets od the search
        :param no_go: co-ordinates that are not optimal to go at current gaestate
        :param scary_ghosts: location of ghosts that can kill
        :param goal_info: naim and value of the goal
        :param safe_if_reached: if the goal makes packman invunerable or win
        :return: updated candidates
        """
        representation = NewCrossroadSearchRep(gstate, goals, no_go, self.distance_map)
        path = ass2.astar(representation, heuristic)  # look for path to a goal

        if self.corner_check:
            new_position = representation.solected_goal  # starts trying to escape somehow
            representation = EscapeRepresentation(gstate, new_position, scary_ghosts, self.distance_map)
            escape_path = ass2.astar(representation, heuristic)
            if escape_path is None:
                g_distance, d, d = find_closest(new_position, scary_ghosts, self.distance_map)
                p_distance = self.distance_map.get_distance(gstate.pacman, new_position)
                if not(safe_if_reached and (g_distance - p_distance) >= 2):
                    candidates = self.update_candidates(candidates, path, goal_info[0] * -200, goal_info[1])
                    return candidates

        candidates = self.update_candidates(candidates, path, goal_info[0], goal_info[1])
        return candidates

    @staticmethod
    def update_candidates(candidates: list, path, weight, name):
        """
        updates candidates such that the value of the goal is added to the move optimal to reach said goal
        :param candidates: list of moves and their values based on goals
        :param path: path to goal
        :param weight: value of goal
        :param name: naim of fond goal
        :return: upddated candidates
        """
        if path is None or len(path) == 0:
            return candidates
        move = path[0]
        for e_move, e_val, e_targets in candidates:
            if e_move == move:
                index = candidates.index(list((e_move, e_val, e_targets)))
                candidates[index][1] += max(weight - (len(path) / 4) ** 3, 0)
                candidates[index][2].append(name)
        return candidates

    def scary_vectors(self, scary_ghosts: list, gstate: gamestate.Gamestate):
        """
        adds possible moves of near ghosts to vectors packman should avoid
        :param scary_ghosts: ghosts that can kill packman
        :param gstate: the state of the game
        :return: all the vectors packman should avoid
        """
        no_go_vectors = []
        for ghost in scary_ghosts:
            moves = gstate.legal_moves_vector(ghost)
            if self.distance_map.get_distance(gstate.pacman, ghost) < 5:  # if the ghost is close
                for move in moves:
                    new_vector = ghost + move.vector
                    if new_vector not in no_go_vectors:
                        no_go_vectors.append(new_vector)  # dont move where a ghost can go during the tick
            else:
                no_go_vectors.append(ghost)
        if gstate.pacman in no_go_vectors:
            no_go_vectors.remove(gstate.pacman)  # packman is not dangerous
        return no_go_vectors


def find_closest(vector: util.Vector, others, distance_map: distancer.Distancer):
    """
    finds the closest element to a vector from a vector list
    :param distance_map: pre computed distances to find actual distances
    :param vector:
    :param others: target list
    :return: tuple of lowest_dis, index_best, total_distances
    """
    lowest_dis = float('inf')
    index_best = 0
    total = 0
    for o in range(len(others)):
        dis = distance_map.get_distance(vector, others[o])
        total += dis
        if dis <= lowest_dis:
            lowest_dis = dis
            index_best = o
    return lowest_dis, index_best, total


class NewCrossroadSearchRep(search.PositionSearchRepresentation):

    solected_goal: util.Vector = None

    def __init__(self, gstate: gamestate.Gamestate, goal: list, no_go: list, distance_map: distancer.Distancer):
        super().__init__(gstate)
        self.goal = goal
        self.no_go = no_go
        self.start_state = gstate.pacman
        self.distance_map = distance_map

    @property
    def start(self) -> util.Vector:
        """
        The initial state of the representation,
        from which searching begins.
        """
        return self.start_state

    def is_goal(self, state: util.Vector):
        """
        sees if the position is in the list of goals
        :param state: position
        :return: boolean
        """
        self.solected_goal = state
        return state in self.goal or len(self.goal) < 1

    def is_no_go(self, state: util.Vector):
        """
        sees if the position is in the non desireable (mainly dangerous positions) that packman shouldn't go
        :param state: position
        :return: boolean
        """
        return state in self.no_go

    def is_terminal(self, state: util.Vector, move: util.Move):
        """
        sees if the position is at a no_go vector or is a goal or is at a crossroad
        :param state: position
        :param move: parent move
        :return: boolean
        """
        moves = self.move_list(state, [move.opposite])
        return (self.is_goal(state) or self.is_no_go(state)) or not (len(moves) == 1 and moves[0] == move)

    def successors(self, state):
        """
        uses a cross road form of successor stops if rossroad or goal is reached
        :param state: packman position
        :return: lits of successor tuples
        """
        successors = []
        start_moves = self.move_list(state, [])
        for move in start_moves:
            new_state = state + util.Move.stop.vector
            moves = []
            while True:
                moves.append(move)
                new_state = new_state + move.vector
                if self.is_terminal(new_state, move):  # post conditional lope brake, if packman can stop here, stop
                    break
            if not self.is_no_go(new_state):  # if this successor doesn't lead to an undesireable vector, use it
                successor = (new_state, moves, len(moves))
                successors.append(successor)
        return successors

    def move_list(self, vector, unwanted_moves):
        """
        finds legal moces for a vector
        :param vector:
        :param unwanted_moves: moves the function will later remove
        :return: list of moves
        """
        moves = []
        for move in util.Move.no_stop:
            test_vector = vector + move.vector
            if not self.walls[test_vector] and move not in unwanted_moves:  # if not illegal move and not unwanted, add
                moves.append(move)
        return moves


class EscapeRepresentation(NewCrossroadSearchRep):
    """
    used to see if a position is likely in-escapable
    """

    def __init__(self, gstate: gamestate.Gamestate, start: util.Vector, no_go: list, distance_map):
        super().__init__(gstate, [None], no_go, distance_map)
        self.start_state = start

    def is_goal(self, state: util.Vector):
        escape_distance = self.distance_map.get_distance(state, self.start_state)
        ghost_distance, d, d = find_closest(state, self.no_go, self.distance_map)
        return len(self.move_list(state, [])) >= 3 and (ghost_distance - escape_distance) >= 1


def heuristic(state, representation: NewCrossroadSearchRep):
    """
    finds the closest out of the representations goals
    :param state:
    :param representation:
    :return: distance to closest goal
    """
    clostest = find_closest(state, representation.goal, representation.distance_map)
    return clostest[0]
