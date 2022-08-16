#game state class
import numpy as np
import copy
from config import params
import evaluation


class GameState:

    def __init__(self):
        self.size = params['board_size']
        self.board = np.zeros((self.size, self.size), dtype=np.byte) #1 is black, 2 is white, 0(#zero) is none
        self.player = "black"
        self.white_score = 0
        self.black_score = 0
        self.cursor_x = self.size//2
        self.cursor_y = self.size//2
        self.is_white_win = False
        self.is_black_win = False
        print("\033[97m")  # change text color to white


    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                character = "＋" if self.board[i][j] == 0 else ("○" if self.board[i][j] == 1 else "●")
                if i==self.cursor_y and j==self.cursor_x:
                    print("\033[32m"+"\033[41m"+character+"\033[97m"+"\033[40m", end='') #커서는 초록색으로 출력
                else:
                    print(character, end='')
            print("")
        print("\nblack: ○, white: ●, empty: ＋ ")
        print("move: w, s, a, d.  put stone: space bar")
        print("current player: {0}({1})".format(self.player,"○" if self.player == "black" else "●"))
        print("black's score: ",self.black_score, "white's score: ", self.white_score)
        print("cursor_y: ", self.cursor_y, "cursor_x: ", self.cursor_x)
        print("black win: {0}, white win: {1}".format(self.is_black_win, self.is_white_win))


    def put_stone(self, row, col, player):
        self.board[row][col] = 1 if player == "black" else 2
        self.change_player()


    def change_player(self):
        self.player = "white" if self.player == "black" else "black"


    def generate_successor(self, action):
        # Check that successors exist
        if self.is_white_win or self.is_black_win: raise Exception('Can\'t generate a successor of a terminal state.')
        row, col = action[0], action[1]
        #copy current state
        gs = copy.deepcopy(self)
        gs.put_stone(row, col, gs.player)
        return gs


    def play_ai(self, player):
        # ai plays gomoku on the given board situation
        pass


    def evaluate(self):

        """
        evaluate heuristic score of the board given player(0 == empty, 1 == black stone, 2 == white stone)
        Note that the order of adv_player and player is reversed since turn changed right after a stone put
        """
        adv_player = self.player
        player = "white" if adv_player == "black" else "black"
        size = params['board_size']
        is_win = False
        # search board horizontally
        total_score = 0
        adv_total_score = 0
        for one_line in self.board:
            score, dictionary = evaluation.eval_one_line(one_line, player)
            is_win = dictionary["is win"] if is_win is False else True
            total_score += score
            adv_score, dictionary = evaluation.eval_one_line(one_line, adv_player)
            is_win = dictionary["is win"] if is_win is False else True
            adv_total_score += adv_score

        # search board vertically
        for one_line in np.transpose(self.board):
            score, dictionary = evaluation.eval_one_line(one_line, player)
            is_win = dictionary["is win"] if is_win is False else True
            total_score += score
            adv_score, dictionary = evaluation.eval_one_line(one_line, adv_player)
            is_win = dictionary["is win"] if is_win is False else True
            adv_total_score += adv_score

        # search board diagonally1 (upper left direction), don't need to compute on corner.(triangular part)
        for i in range(-size + 5, size - 4):
            idx = i
            one_line = np.diag(self.board, idx)
            score, dictionary = evaluation.eval_one_line(one_line, player)
            is_win = dictionary["is win"] if is_win is False else True
            total_score += score
            adv_score, dictionary = evaluation.eval_one_line(one_line, adv_player)
            is_win = dictionary["is win"] if is_win is False else True
            adv_total_score += adv_score

        # search board diagonally2 (upper right direction), don't need to compute on corner.(triangular part)
        board_flipped = np.fliplr(self.board)
        for i in range(-size+5, size - 4):
            idx = i
            one_line = np.diag(board_flipped, idx)
            score, dictionary = evaluation.eval_one_line(one_line, player)
            is_win = dictionary["is win"] if is_win is False else True
            total_score += score
            adv_score, dictionary = evaluation.eval_one_line(one_line, adv_player)
            is_win = dictionary["is win"] if is_win is False else True
            adv_total_score += adv_score

        if player == "black" and is_win:
            self.is_black_win = True
        if player == "white" and is_win:
            self.is_white_win = True
        value = total_score - adv_total_score * 0.9 # put more value on attacking than defending
        adv_value = adv_total_score - total_score * 0.9
        if player == "black":
            self.black_score = value
            self.white_score = adv_value
        else:
            self.black_score = value
            self.white_score = adv_value
        return value


