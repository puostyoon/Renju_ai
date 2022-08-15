import game_state, evaluation, utils

class TreeSearch():

    def __init(self, gs: game_state.GameState, depth):
        self.gs = gs
        self.depth = depth

    def getAction(self, gs):
        #get minmax action based on tree search

        def value(gs, cur_level, depth = self.depth):
            # return (value, action) of the tree node
            if cur_level == depth*


