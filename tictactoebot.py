from copy import deepcopy


def print_current_playing_field(current_playing_field: list):
    for i in range(3):
        for j in range(3):
            symbol = current_playing_field[i][j]
            if symbol == 0:
                symbol = '_'
            elif symbol == 1:
                symbol = "X"
            elif symbol == -1:
                symbol = "O"
            print(symbol, end=' ')
        print('\n')


# 'A1' -> (1, 1)
def convert_player_code_to_row_and_columns(player_move: str) -> tuple:
    letters_to_numbers = {'A': 0, 'B': 1, 'C': 2}
    return letters_to_numbers[player_move[0]], int(player_move[1]) - 1


def step(updated_playing_field: list, player_move: tuple, current_player: int):
    row = player_move[0]
    column = player_move[1]
    if updated_playing_field[row][column] == 0:
        updated_playing_field[row][column] = current_player
        return updated_playing_field
    else:
        return 0


def diagonal_win(current_playing_field: list) -> int:
    diag_sum = 0
    diag2_sum = 0

    for i in range(3):
        diag_sum += current_playing_field[i][i]
        diag2_sum += current_playing_field[i][2 - i]

    if abs(diag_sum) == 3:
        return diag_sum // 3
    if abs(diag2_sum) == 3:
        return diag2_sum // 3


def horizontal_vertical_win(current_playing_field: list) -> int:
    for row in range(3):
        vertical_sum = 0
        horizontal_sum = 0
        for column in range(3):
            horizontal_sum += current_playing_field[row][column]
            vertical_sum += current_playing_field[column][row]

        if abs(horizontal_sum) == 3:
            return horizontal_sum // 3
        if abs(vertical_sum) == 3:
            return vertical_sum // 3


def check_winning_conditions(current_playing_field: list) -> int:
    diagonal_check = diagonal_win(current_playing_field)
    horizontal_vertical_check = horizontal_vertical_win(current_playing_field)
    if diagonal_check == 1 or horizontal_vertical_check == 1:
        return 1
    elif diagonal_check == -1 or horizontal_vertical_check == -1:
        return -1
    else:
        return 0


def define_player_to_move(step_count: int):
    if step_count % 2 == 0:
        return 1
    else:
        return -1


def decorated_player_to_move(current_player: int):
    if current_player == 1:
        return 'X'
    else:
        return 'O'


def find_free_cells(field):
    free_cells = []
    for i in range(3):
        for j in range(3):
            if field[i][j] == 0:
                free_cells.append((i, j))
    return free_cells


def minimax(current_field: list, depth, player, best_moves: list):
    win = check_winning_conditions(current_field)
    if depth == 0 or win:
        return win, best_moves

    if player == 1:
        maxEval = -10e6
        free_cells = find_free_cells(current_field)
        for cell in free_cells:
            updated_field = deepcopy(current_field)
            updated_field[cell[0]][cell[1]] = player

            pos_eval = minimax(updated_field, depth - 1, -1, best_moves)[0]
            best_moves.append((cell, pos_eval, depth, player))
            if pos_eval > maxEval:
                maxEval = pos_eval
        return maxEval, best_moves

    else:
        minEval = 10e6
        free_cells = find_free_cells(current_field)
        for cell in free_cells:
            updated_field = deepcopy(current_field)
            updated_field[cell[0]][cell[1]] = player

            pos_eval = minimax(updated_field, depth - 1, 1, best_moves)[0]
            best_moves.append((cell, pos_eval, depth, player))
            if pos_eval < minEval:
                minEval = pos_eval
        return minEval, best_moves


def main():
    playing_field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    step_amount = 0
    while True:
        print_current_playing_field(playing_field)
        current_player = define_player_to_move(step_amount)

        winner = check_winning_conditions(playing_field)
        if winner != 0:
            print(f'Player "{decorated_player_to_move(winner)}" wins!')
            if winner == -1:
                print('Oh you such a newbie, you were defeated by a BOT, bruh. You fool.')
            break
        elif step_amount == 9 and not winner:
            print(f"It's a tie")
            break
        if current_player == 1:
            player_move = input(f'Player "{decorated_player_to_move(current_player)}" to move: ')
            stepan = step(playing_field, convert_player_code_to_row_and_columns(player_move), current_player)
        else:  # bot_step
            result = minimax(playing_field, 9 - step_amount, -1, [])
            best_result = [(), -10e6, -10e6, -1]
            for i in range(len(result[1])):
                if result[1][i][3] == -1 and result[1][i][1] == result[0]:
                    good_result = result[1][i]
                    if good_result[2] > best_result[2]:
                        best_result = good_result
            print(result[0], "настроение бота :(")
            stepan = step(playing_field, best_result[0], current_player)
        while True:
            if stepan != 0:
                playing_field = stepan
                step_amount += 1
                break
            else:
                print('You fucking stupid dogshit, this fucking cell is occupied by another asshole')
                player_move = input(f'Player "{decorated_player_to_move(current_player)}" to move: ')
                stepan = step(playing_field, convert_player_code_to_row_and_columns(player_move), current_player)


main()