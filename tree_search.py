import game_state, evaluation, utils
from game_state import GameState
from config import params

class TreeSearch:

    def __init__(self, gs: game_state.GameState, depth=params['tree_search_depth']):
        self.gs = gs
        self.depth = depth
        self.eval_dict = dict()

    def get_action(self, gs):
        #get minmax action based on tree search

        def value(gs: GameState, cur_level, alpha, beta, depth=self.depth):
            """ return (value, action) of the tree node
            cur_level = current level of tree searching, starts from 1.
            """
            if cur_level == depth*2+1 or gs.is_white_win or gs.is_black_win:
                key = (tuple(gs.board.flatten()), gs.player)
                if key in self.eval_dict:
                    return self.eval_dict[key]
                else:
                    self.eval_dict[key] = [gs.evaluate()]
                    return [gs.evaluate()]
            elif (cur_level-1)%2 == 0:
                #min node
                return min_value(gs, cur_level, alpha, beta)
            else:
                #max node
                return max_value(gs, cur_level, alpha, beta)

        def max_value(gs: GameState, cur_level, alpha, beta):
            """ return (value, action) tuple. score is maximum score among scores of successors
            and action is the action that results in the max score.
            """
            best_score = -float("inf")
            legal_moves = utils.return_legal_actions(gs)
            for action in legal_moves:
                successor = gs.generate_successor(action)
                successor_score = value(successor, cur_level+1, alpha, beta)[0]
                if successor_score>=beta:
                    return (successor_score, action)
                elif successor_score>best_score:
                    best_score = successor_score
                    best_action = action
                    alpha = successor_score if successor_score>alpha else alpha
            return (best_score, best_action)

        def min_value(gs: GameState, cur_level, alpha, beta):
            worst_score = float("inf")
            legal_moves = utils.return_legal_actions(gs)
            for action in legal_moves:
                succeesor = gs.generate_successor(action)
                succeesor_score = value(succeesor, cur_level+1, alpha, beta)[0]
                if succeesor_score <= alpha:
                    return (succeesor_score, action)
                elif succeesor_score<worst_score:
                    worst_score=succeesor_score
                    worst_action = action
                    beta = succeesor_score if succeesor_score<beta else beta
            return (worst_score, worst_action)
        score, action = value(gs, 1, -float("inf"), float("inf"))
        return action