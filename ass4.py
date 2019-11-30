# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
from pacman import agents, gamestate, util
import collections


class BetterReflexAgent(agents.ReflexAgent):
    def evaluate(self, gstate: gamestate.Gamestate, move: util.Move):
        """
        Adapted from the pre-existing solution, for the new state representation
        Use only as inspiration
        """
        gstate.apply_move(0, move)
        return better_evaluate(gstate)


# These algorithms are straightforward translations of the algorithms from the book
class MinimaxAgent(agents.AdversarialAgent):
    def move(self, gstate: gamestate.Gamestate) -> 'enum<Move>':
        """
        Finds the next move.

        :param gstate: (gamestate.Gamestate) the current gamestate

        :returns: (enum<Move>) the move to make
        """
        move_values = [(move, self.minimax(gstate.successor(0, move), 0, False))
                       for move in gstate.legal_moves_id(0) if move != util.Move.stop]
        return max(move_values, key=lambda x: x[1])[0]

    def minimax(self, state: gamestate.Gamestate, depth: int, is_maximizing: bool) -> int:
        """
        Evaluates a potential move.

        :param state: (gamestate.Gamestate) gamestate if the move to be evaluated is made
        :param depth: (int) depth of the search
        :param is_maximizing: (bool) True if maximizing

        :returns: (int) value of the move
        """
        if depth == self.depth or state.gameover:
            return self.evaluate(state)

        if is_maximizing:
            return max(self.minimax(s, depth, False) for s in state.successors(0))
        else:
            return min(self.minimax(s, depth+1, True) for s in state.successors(1))


class AlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate: gamestate.Gamestate) -> 'enum<Move>':
        """
        Finds the next move.

        :param gstate: (gamestate.Gamestate) the current gamestate

        :returns: (enum<Move>) the move to make
        """
        alpha = float('-inf')
        move_values = []

        for move in gstate.legal_moves_id(0):
            if move != util.Move.stop:
                value = self.alphabeta(gstate.successor(
                    0, move), 0, alpha, float('inf'), False)
                move_values.append((move, value))
                alpha = max(alpha, value)

        return max(move_values, key=lambda x: x[1])[0]

    def alphabeta(self, gstate: gamestate.Gamestate, depth: int, alpha: int, beta: float, is_maximizing: bool):
        """
        Evaluates a potential move.

        :param state: (gamestate.Gamestate) gamestate if the move to be evaluated is made
        :param depth: (int) depth of the search
        :param alpha: (int) pruning alpha
        :param beta: (float) pruning beta
        :param is_maximizing: (bool)

        :returns: (int) value of the move
        """
        if depth == self.depth or gstate.gameover:
            return self.evaluate(gstate)

        if is_maximizing:
            best_value = float('-inf')
            for successor in gstate.successors(0):
                best_value = max(best_value, self.alphabeta(
                    successor, depth, alpha, beta, False))
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        else:
            best_value = float('inf')
            for successor in gstate.successors(1):
                best_value = min(best_value, self.alphabeta(
                    successor, depth+1, alpha, beta, True))
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
        return best_value


def better_evaluate(gstate: gamestate.Gamestate) -> int:
    """
    Adapted from the pre-existing solution, for the new state representation
    Use only as inspiration, because it's actually terrible

    :param gstate: (gamestate.Gamestate) the gamestate to evaluate

    :returns: (int) the value of the gamestate
    """
    newPos = gstate.pacman
    newFood = gstate.dots.list()
    ghostPositions = gstate.ghosts
    newScaredTimes = gstate.timers

    # Successor state is a win state
    if gstate.win:
        return float('inf')
    elif gstate.loss:
        return float('-inf')

    score = 0
    # Check for collissions with ghosts
    # High positive score if Pacman can easily eat a ghost (i.e. one very nearby)
    # High negative score if Pacman can easily be eaten by ghost (i.e. one very nearby)
    for index, ghostPosition in enumerate(ghostPositions):
        ghostScaredTime = newScaredTimes[index]
        distanceToGhost = util.manhattan(newPos, ghostPosition)
        if ghostScaredTime > 0:
            # Pacman can eat the ghost
            if distanceToGhost < 1:
                score = float('inf')
                break
        else:
            # Pacman shouldn't risk it
            if distanceToGhost < 2:
                score = float('-inf')
                break

    # Calculate food distance over all food
    # N.B. better would be to use the minimum spanning tree distance
    foodDistance = 0
    for food in newFood:
        foodDistance += util.manhattan(newPos, food)
    # N.B. high foodDistance is bad, so we invert (1/x) it so high distances score low
    #  using 10/foodDistance means we score 1 for having all the food within 10 steps of pacman
    score = score - foodDistance

    # Calculate ghost distance over all ghosts
    ghostDistance = 0
    for ghost in ghostPositions:
        ghostDistance += util.manhattan(newPos, ghost)
    # N.B. high ghostDistance is good, so don't invert that.  *But* nearby ghosts are bad so scale strongly
    #   mult by 30 means we score and additional 30 for every unit a ghost is further away
    #   this is equivalent to saying that its worth taking 30 steps for each food pellet to avoid a ghost
    score += (4**(1/ghostDistance))

    # N.B. low number food still to eat is good, so invert so low food to go scores high
    score = score - len(newFood)**3
    return score


class MultiAlphabetaAgent(agents.AdversarialAgent):
    # The only thing that changes w.r.t. alpha-beta pruning above
    # is that we have an index for the agent rather than True/False,
    # where depth is only increased for the last ghost agent,
    # and we have a separate beta for each agent. We prune if any
    # agent's beta is smaller or equal than alpha.

    def move(self, gstate: gamestate.Gamestate) -> 'enum<Move>':
        """
        Finds the next move.

        :param gstate: (gamestate.Gamestate) the current gamestate

        :returns: (enum<Move>) the move to make
        """
        alpha = float('-inf')
        beta = float('inf')
        move_values = []

        for move in gstate.legal_moves_id(0):
            if move != util.Move.stop:
                value = self.alphabeta(
                    gstate.successor(0, move), 0, alpha, beta, 1)
                move_values.append((move, value))
                alpha = max(alpha, value)

        return max(move_values, key=lambda x: x[1])[0]

    def alphabeta(self, gstate: gamestate.Gamestate, depth: int, alpha: int, beta: float, agent_id: int) -> int:
        """
        Evaluates a potential move.

        :param state: (gamestate.Gamestate) gamestate if the move to be evaluated is made
        :param depth: (int) depth of the search
        :param alpha: (int) pruning alpha
        :param beta: (float) pruning beta
        :param agent_id: (int) recursion through ghosts

        :returns: (int) value of the move
        """
        if depth == self.depth or gstate.gameover:
            return self.evaluate(gstate)

        if agent_id == 0:
            best_value = float('-inf')
            for successor in gstate.successors(0):
                best_value = max(best_value, self.alphabeta(
                    successor, depth, alpha, beta, agent_id + 1))
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
        else:
            best_value = float('inf')
            for successor in gstate.successors(agent_id):
                best_value = min(best_value, self.alphabeta(successor, depth + (agent_id + 1) // len(gstate.agents),
                                                            alpha, beta, (agent_id + 1) % len(gstate.agents)))
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
        return best_value
