import numpy as np
from config import params
import evaluation


def return_legal_actions(game_state, player: str)->list:
    # following the Renju rule, detect legal actions and return list of legal actions
    #return list of legal actions [(pos_y,,pos_x), (pos_y2, pos_x2), .... ] where pos_x, pos_y are integers
    size = params['size']
    board_with_pad = np.zeros((size+4, size+4), dtype=np.byte)
    board_with_pad[2:size+2, 2:size+2] = game_state.board[:, :]
    legal_actions = list()
    for pos_y in range(size):
        for pos_x in range(size):

            neighbor_board = board_with_pad[pos_y:pos_y+4, pos_x:pos_x+4]
            neighbor_board[2][2] = 0
            if neighbor_board.sum() == 0: #no adjacent stones, don't need to search for this action
                continue

            _, cur_dict = evaluation.evaluate(game_state.board, player)
            cur_three_without_block = cur_dict["three without block"]
            cur_four = cur_dict["four"]

            future_game_state = game_state.copy()
            future_game_state.put_stone(pos_y, pos_x)
            _, future_dict = evaluation.evaluate(future_game_state.board, player)
            future_three_without_block = future_dict["three without block"]
            future_four = future_dict["four"]
            future_six = future_dict["six in a row"]

            if (future_three_without_block - cur_three_without_block >= 2) or (future_six is True) or (
                future_four - cur_four >= 2):
                continue

            legal_actions.append((pos_y, pos_x))
        #end
    #end
    return legal_actions
#end



