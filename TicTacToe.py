def show_board():
    
    print(' ___________')
    for i in range(3):
        print('|', board[0+i*3], '|', board[1+i*3], '|', board[2+i*3], '|')
    print(' -----------')


def input_check(player_move):

    while True:
        player_input = input(f'ВВедите номер клетки, куда поставить {player_move} ')
        if not player_input.isdigit():
            print('Введите цифру!\n')
            continue
        player_input = int(player_input)
        if 1 <= player_input <= 9:
            if str(board[player_input-1]) not in "XO":
                board[player_input-1] = player_move
                break
            else:
                print('Данная клетка уже занята. Введите номер свободной!\n')
        else:
            print('Число должно быть в диапазоне от 1 до 9!\n')


def check_win():

    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            print(f'{board[each[0]]} одержал победу!')
            show_board()
            return True
    return False


board = list(range(1, 10))
counter = 0
while True:
    show_board()
    if counter % 2 == 0:
        input_check("X")
    else:
        input_check("O")
    counter += 1
    if counter > 4:
        if check_win():
            break
    if counter == 9:
        print("Ничья!")
        break
