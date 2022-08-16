import copy
import os
import time
import msvcrt
import game_state
from tree_search import TreeSearch
import evaluation


def renju(game_mode, player):
    gs = game_state.GameState()
    gs.print_board()
    gs.player = player
    search_agent = TreeSearch(gs)
    player_idx = 0 if player == "black" else 1
    while True:
        if game_mode == 2 or game_mode == 3:
            if player_idx % 2 == 0:
                while True:
                    row, col = gs.cursor_y, gs.cursor_x
                    os.system('cls')
                    gs.print_board()
                    input_key = msvcrt.getch()
                    if input_key == b"w" and gs.cursor_y > 0:
                        gs.cursor_y -= 1
                    elif input_key == b's' and gs.cursor_y + 1 < gs.size:
                        gs.cursor_y += 1
                    elif input_key == b'a' and gs.cursor_x > 0:
                        gs.cursor_x -= 1
                    elif input_key == b'd' and gs.cursor_x + 1 < gs.size:
                        gs.cursor_x += 1
                    elif input_key == b' ':  # space bar
                        break
                    elif input_key == b'1':
                        gs.player = "black"
                        break
                    elif input_key == b'2':
                        gs.player = "white"
                        break
            else:
                print("A.I. is now thinking for next action....")
                row, col = search_agent.get_action(gs)
                gs.cursor_y, gs.cursor_x = row, col
        elif game_mode == 1:
            print("A.I. is now thinking next action....")
            row, col = search_agent.get_action(gs)
            gs.cursor_y, gs.cursor_x = row, col
        player_idx = player_idx + (2 if game_mode == 3 else 1)
        gs.put_stone(row, col, gs.player)
        gs.evaluate()
        os.system('cls')
        gs.print_board()
        if gs.is_black_win:
            print("!!black win!!")
            break
        elif gs.is_white_win:
            print("!!white win!!")
            break


def test():
    start_time = time.time()
    gs = game_state.GameState()
    for i in range(1000):
        gs.evaluate()
        gs.put_stone(0, 0, gs.player)
    end_time = time.time()
    time_spent = end_time - start_time
    print("time spent: ", time_spent)


def config():
    game_mode = int(input("\tChoose game mode\n\n\t1) A.I. self competition\n\t2) A.I. vs player\n\t3) player vs player\n\n\tEnter input: "))
    player = "black"
    os.system("cls")
    if game_mode == 2:
        player = int(input("\tChoose your player\n\n\t1)black\t2)white\n\n\tEnter input: "))
        player = "white" if player == 2 else "black"
    os.system("cls")
    return game_mode, player

if __name__ == '__main__':
    print("\n\n\n\t\tPress any key to start\n\n\n", end='')
    msvcrt.getch()
    os.system("cls")
    #test()
    game_mode, player = config()
    renju(game_mode, player)



