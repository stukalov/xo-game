import random

lines = ((0, 1, 2),
         (3, 4, 5),
         (6, 7, 8),
         (0, 3, 6),
         (1, 4, 7),
         (2, 5, 8),
         (0, 4, 8),
         (2, 4, 6))

def print_game(field):
    output = [
        '      1     2     3   (x)',
        '   |-----|-----|-----|',
        f' 1 |  {field[0]}  |  {field[1]}  |  {field[2]}  |',
        '   |-----|-----|-----|',
        f' 2 |  {field[3]}  |  {field[4]}  |  {field[5]}  |',
        '   |-----|-----|-----|',
        f' 3 |  {field[6]}  |  {field[7]}  |  {field[8]}  |',
        '   |-----|-----|-----|',
        '(y)'
    ]
    print('\n'.join(output))

def has_one_free_cell(field, xo):
    for line in lines:
        c_xo = 0
        c_empty = 0
        for i in line:
            if field[i] == xo:
                c_xo += 1
            elif field[i] == ' ':
                c_empty += 1
        if c_xo == 2 and c_empty == 1:
            for i in line:
                if field[i] == ' ':
                    return i+1

def random_cell(field):
    free_cell = [i for i in range(9) if field[i] == ' ']
    step = random.choice(free_cell)
    return step+1

def bot_step(field, user, bot):
    # получает и возвращает индекс увеличенный на 1 для простоты проверки в следующей строчке
    return has_one_free_cell(field, bot) or has_one_free_cell(field, user) or random_cell(field)

def user_step(field):
    inp = input('Введите координаты вашего хода X и Y через пробел: ')
    xy = inp.split()
    if len(xy) != 2:
        raise ValueError('Указано неверное количество координат')
    try:
        x, y = list(map(int, xy))
    except ValueError as e:
        raise ValueError('Одна из координат не число')
    if x not in [1, 2, 3]:
        raise ValueError('Координата X за пределами значений. Для X укажите 1, 2 или 3')
    if y not in [1, 2, 3]:
        raise ValueError('Координата Y за пределами значений. Для Y укажите 1, 2 или 3')
    cell = (y - 1) * 3 + (x - 1)
    if field[cell] != ' ':
        raise ValueError(f'Клетку {x}:{y} выбрать нельзя, в ней уже есть "{field[cell]}"')
    return cell

def check_win(xo, field):
    for line in lines:
        if all([field[line[0]] == xo, field[line[1]] == xo, field[line[2]] == xo]):
            return xo

def check_end_field(field):
    return all([field[i] != ' ' for i in range(9)])

def check_end_game(field, user, bot):
    won = check_win(user, field) or check_win(bot, field)
    return check_end_field(field) or won, won

def choice_XO():
    print('Введите "Х", чтобы ходить первым.')
    print('Введите "0", чтобы ходить вторым.')
    print('Или любой другой символ для выхода ')
    inp = input('Выберите за кого вы играете: ').upper()
    if inp in ['X', 'Х']: # латинская или русская
        return 'X'
    elif inp in ['0', 'O', 'О']: # цифра, латинская или русская
        return '0'

def play(field, user, bot):
    play_step = 'X'
    if play_step == user:
        print_game(field)
    while True:
        try:
            if play_step == user:
                print('\nВаш ход:')
                field[user_step(field)] = user
                play_step = bot
            else:
                print('\nХод компьютера:')
                field[bot_step(field, user, bot)-1] = bot
                play_step = user

            print_game(field)
            end, won = check_end_game(field, user, bot)
            if end:
                break
        except ValueError as e:
            print(e)

    if won == user:
        print('Вы выиграли')
    elif won == bot:
        print('Выиграл компьютер')
    else:
        print('Ничья')

print('Приветствую Вас в игре Крестики-Нолики\n')
while True:
    try:
        start = choice_XO()
        if start is None:
            break
        play([' ' for i in range(9)], *('X', '0') if start == 'X' else ('0', 'X'))
        print('\n\n\nПоиграем еще раз?\n')
    except KeyboardInterrupt:
        print('')
        break
    except Exception:
        print('Произошла ошибка\n')

print('Игра закончена. Ждем Вас снова\n')


