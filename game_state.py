#game state class
import numpy as np
from config import params
import evaluation


class GameState():

    def __init__(self):
        self.size = params['board_size']
        self.board = np.zeros((self.size, self.size), dtype=np.byte) #1 is black, 2 is white, 0(#zero) is none
        self.player = 0
        self.cursor_x = self.size//2
        self.cursor_y = self.size//2
        print("\033[97m")  # 글자 색 변경

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
        print("black's score: ",evaluation.evaluate(self.board, "black"), "white's score: ", evaluation.evaluate(self.board, "white"))
        print("cursor_y: ",self.cursor_y, "cursor_x: ",self.cursor_x)


    def put_stone(self, row, col, player):
        self.board[row][col] = 1 if player == "black" else 2


    def play_ai(self, player):
        # ai plays gomoku on the given board situation
        pass
