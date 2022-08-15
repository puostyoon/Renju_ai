import os
import msvcrt
import game_state
import evaluation


def renju():
    gs = game_state.GameState()
    gs.print_board()
    gs.player = "black"
    while True:
        while True:
            input_key = msvcrt.getch()
            if input_key == b"w" and gs.cursor_y > 0:
                gs.cursor_y -= 1
            elif input_key == b's' and gs.cursor_y+1 < gs.size:
                gs.cursor_y += 1
            elif input_key == b'a'and gs.cursor_x > 0:
                gs.cursor_x -= 1
            elif input_key == b'd'and gs.cursor_x+1 < gs.size:
                gs.cursor_x += 1
            elif input_key == b' ':  # space bar
                break
            elif input_key == b'1':
                gs.player = "black"
                break
            elif input_key == b'2':
                gs.player = "white"
                break
            os.system('cls')
            gs.print_board()
        row, col = gs.cursor_y, gs.cursor_x
        gs.put_stone(row, col, gs.player)
        gs.player = "white" if gs.player == "black" else "black"
        os.system('cls')
        gs.print_board()
        if evaluation.evaluate(gs.board,"white")>=1000 or evaluation.evaluate(gs.board, "black")>=1000:
            break


if __name__ == '__main__':
    print("\n\n\n\t\t\tEnter any key to start\n\n\n", end='')
    msvcrt.getch()
    os.system("cls")
    renju()



