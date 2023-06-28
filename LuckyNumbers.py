import tkinter
from tkinter import ttk, Toplevel
import random
import copy
import time
import tkinter.font as font

# поля игрока и бота
desk_player = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
desk_comp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# фишки на столе
table_cards = []

levels = ["Без подсказок", "С блокировкой неверных ходов", "С подсказками без блокировки"]

# цвета кнопок игрока
color_player = [['grey', 'grey', 'grey', 'grey'], ['grey', 'grey', 'grey', 'grey'], ['grey', 'grey', 'grey', 'grey'],
                ['grey', 'grey', 'grey', 'grey']]

# колода
cards = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16,
         17, 17, 18, 18, 19, 19, 20, 20]

# для выбора карт со стола
cards_choice = []

cur_step_number = [0]

state_of_game = {'state': "wait", 'step': 0, 'block': True, 'result': 'no result', 'move': 'player', 'level_game': 0,
                 'time': 0}

chip_comp = {'prev': 0, 'prev_in_table': 0}


# очистка рабочего поля после конца игры
def clear_desk():
    for i in range(4):
        for j in range(4):
            desk_player[i][j], desk_comp[i][j] = 0, 0
            color_player[i][j] = 'grey'
    for i in reversed(range(len(cards_choice))):
        cards.append(cards_choice[i])
        cards_choice.pop(i)
    button_deck['text'] = 'Осталось ' + str(len(cards)) + ' карт(-а, -ы)'
    label_num['text'] = 'Выберите режим'
    label_table['text'] = 'Стол пуст'
    table_cards.clear()
    table_player()
    table_comp()


# проверка массива на правильность -- выполняется ли правило возрастания в строках и столбцах
def check_wrong_completed(mass):
    for i in range(4):
        prev = mass[i][0]
        for j in range(1, 4):
            if mass[i][j] != 0:
                if mass[i][j] > prev:
                    prev = mass[i][j]
                else:
                    return False
    for j in range(4):
        prev = mass[0][j]
        for i in range(1, 4):
            if mass[i][j] != 0:
                if mass[i][j] > prev:
                    prev = mass[i][j]
                else:
                    return False
    return True


# изменение числа в ячейке на поле игрока
def change_number(x, y, color):
    if state_of_game['block'] or label_num['text'] == 'Ваш ход':
        return
    if color == 'grey':
        if state_of_game['state'] == 'diagonal':
            if x != y:
                if state_of_game['level_game'] == 0 or state_of_game['level_game'] == 2:
                    state_of_game['result'] = 'lost'
                    state_of_game['block'] = True
                    state_of_game['state'] = 'wait'
                    get_result()
                    clear_desk()
                    return
                else:
                    return
        else:
            temp_mass = copy.deepcopy(desk_player)
            temp_mass[x][y] = cur_step_number[0]
            if not check_wrong_completed(temp_mass):
                if state_of_game['level_game'] == 1:
                    return
                state_of_game['result'] = 'lost'
                state_of_game['block'] = True
                state_of_game['state'] = 'wait'
                get_result()
                clear_desk()
                return
    if desk_player[x][y] != 0:
        table_cards.append(str(desk_player[x][y]))
        label_table["text"] = 'На столе ' + ", ".join(table_cards)
    desk_player[x][y] = cur_step_number[0]
    state_of_game['block'] = True
    state_of_game['move'] = 'comp'
    change_color_after_move(x, y)
    state_of_game['step'] += 1
    table_player()


# изменение цвета ячейки, где был последний ход (она зеленая, остальные - серые)
def change_color_after_move(x, y):
    for i in range(4):
        for j in range(4):
            if i == x and j == y:
                color_player[i][j] = 'green'
            else:
                color_player[i][j] = 'grey'


# изменение цвета на поле игрока
def change_color():
    if state_of_game['state'] == 'main':
        for i in range(4):
            temp_mass = desk_player[i]
            temp_color = []
            max_in_line = max(temp_mass)
            min_in_line = min(temp_mass)
            for k in range(4):
                if max_in_line > temp_mass[k] >= cur_step_number[0]:
                    max_in_line = temp_mass[k]
                if min_in_line < temp_mass[k] <= cur_step_number[0]:
                    min_in_line = temp_mass[k]
            max_index = temp_mass.index(max_in_line)
            min_index = temp_mass.index(min_in_line)
            for j in range(4):
                if max_in_line < cur_step_number[0]:
                    if j < max_index:
                        temp_color.append('grey')
                    else:
                        temp_color.append('yellow')
                elif max_in_line > cur_step_number[0]:
                    if j > max_index:
                        temp_color.append('grey')
                    elif min_in_line == 0 or min_in_line != 0 and j >= min_index:
                        temp_color.append('yellow')
                    else:
                        temp_color.append('grey')
                else:
                    temp_color.append('grey')
            color_player[i] = temp_color
        for j in range(4):
            temp_mass = [desk_player[0][j], desk_player[1][j], desk_player[2][j], desk_player[3][j]]
            max_in_col = max(temp_mass)
            min_in_col = min(temp_mass)
            for k in range(4):
                if max_in_col > temp_mass[k] >= cur_step_number[0]:
                    max_in_col = temp_mass[k]
                if min_in_col < temp_mass[k] <= cur_step_number[0]:
                    min_in_col = temp_mass[k]
            max_index = temp_mass.index(max_in_col)
            min_index = temp_mass.index(min_in_col)
            for i in range(4):
                if color_player[i][j] != 'grey':
                    if max_in_col < cur_step_number[0]:
                        if i < max_index:
                            color_player[i][j] = 'grey'
                        else:
                            color_player[i][j] = 'yellow'
                    elif max_in_col > cur_step_number[0]:
                        if i > max_index:
                            color_player[i][j] = 'grey'
                        elif min_in_col == 0 or (min_in_col != 0 and i >= min_index):
                            color_player[i][j] = 'yellow'
                        else:
                            color_player[i][j] = 'grey'
                    else:
                        color_player[i][j] = 'grey'
    elif state_of_game['state'] == 'diagonal':
        for i in range(4):
            if desk_player[i][i] == 0:
                color_player[i][i] = 'yellow'
            else:
                color_player[i][i] = 'grey'


# выбор режима
def selected():
    if state_of_game.get('state') == 'wait':
        selection = combobox.get()
        if selection == '':
            selection = levels[0]
        state_of_game['level_game'] = levels.index(selection)
        state_of_game['state'] = 'diagonal'
        state_of_game['block'] = False
        label_num['text'] = 'Ваш ход'
        state_of_game['time'] = time.time()


# нажатие на колоду - генератор случайного числа у игрока
def click_func():
    if not state_of_game['block'] and label_num['text'] == 'Ваш ход' and len(cards) > 0:
        cur_index = random.randint(0, len(cards) - 1)
        cur_number = cards.pop(cur_index)
        cur_step_number[0] = cur_number
        cards_choice.append(cur_number)
        label_num['text'] = 'Ваше число ' + str(cur_number)
        button_deck['text'] = 'Осталось ' + str(len(cards)) + ' карт(-а, -ы)'
        if not state_of_game['level_game'] == 0:
            change_color()
            table_player()


# вывод результаты игры
def get_result():
    win = True
    lose = True
    for i in range(4):
        if 0 in desk_player[i]:
            win = False
            break
    for i in range(4):
        if 0 in desk_comp[i]:
            lose = False
            break
    if state_of_game['result'] == 'no result':
        if win:
            state_of_game['result'] = 'win'
        elif lose:
            state_of_game['result'] = 'lose'
    if not state_of_game['result'] == 'no result':
        end = time.time() - state_of_game['time']
        top = Toplevel(root)
        if state_of_game['result'] == 'win':
            text_result = 'Победа!'
        else:
            text_result = 'Проигрыш!'
        if win is False and lose is False:
            text_result += '\nПричина: ошибка хода'
        elif win is False and lose is True:
            text_result += '\nПричина: победа компьютера'

        sum_player = sum([len(line) - line.count(0) for line in desk_player])
        sum_comp = sum([len(line) - line.count(0) for line in desk_comp])

        if state_of_game['result'] == 'win':
            count = (state_of_game['step'] - 1) * 2 + 1
            count_player = state_of_game['step']
        elif state_of_game['result'] == 'lost' and lose is False:
            count_player = state_of_game['step'] + 1
            count = (state_of_game['step']) * 2 + 1
        else:
            count = state_of_game['step'] * 2
            count_player = state_of_game['step']
        text_result += '\nОбщее количество ходов: ' + str(count)
        text_result += '\n\t из них ходы игрока: ' + str(count_player)
        text_result += '\n\tходы компьютера: ' + str(count - count_player)

        text_result += '\nКоличество использованных фишек: ' + str(sum_player + sum_comp + len(table_cards))
        text_result += '\n\tРасставлено пользователем фишек: ' + str(sum_player)
        text_result += '\nВремя: ' + str(end) + ' seconds'
        ttk.Label(top, text=text_result).pack()
        top.transient(root)
        top.grab_set()
        top.focus_set()
        top.wait_window()
        state_of_game['result'] = 'no result'
        state_of_game['step'] = 0
        state_of_game['move'] = 'player'
        state_of_game['block'] = True
        state_of_game['state'] = 'wait'
        clear_desk()


# остановить игру на количество секунд - чтобы игрок видел, какую карту взял бот
def tk_sleep(self, t) -> None:
    self.after(int(t * 1000), self.quit)
    self.mainloop()


# поиск наилучшего хода бота с картами со стола
def find_best_move_with_cards_on_table(is_reversed=False):
    x, y, min_difference = 0, 0, 20
    x_with_0, y_with_0, min_dif_with_0 = 0, 0, 20
    temp_number = 0
    temp_number_with_0 = 0
    diagonal = [desk_comp[0][0], desk_comp[1][1], desk_comp[2][2], desk_comp[3][3]]
    mass_for_range = [0, 1, 2, 3]
    if is_reversed:
        mass_for_range.reverse()
    if all(diagonal[i] < diagonal[i + 1] for i in range(len(diagonal) - 1)):
        diagonal_norma = True
        for k in range(len(table_cards)):
            for i in mass_for_range:
                for j in mass_for_range:
                    temp_mass = copy.deepcopy(desk_comp)
                    old_with_0 = temp_mass[i][j]
                    temp_mass[i][j] = int(table_cards[k])
                    if check_wrong_completed(temp_mass):
                        dif = 0
                        last_num = temp_mass[i][0]
                        for d in range(j - 1, 0, -1):
                            if temp_mass[i][d] == 0:
                                dif += 1
                            else:
                                last_num = temp_mass[i][d]
                                break
                        dif_col = 0
                        last_num_col = temp_mass[0][j]
                        for d in range(i - 1, 0, -1):
                            if temp_mass[d][j] == 0:
                                dif_col += 1
                            else:
                                last_num_col = temp_mass[d][j]
                                break
                        if (dif < temp_mass[i][j] - last_num or dif == 0) and \
                                (dif_col < temp_mass[i][j] - last_num_col or dif_col == 0):
                            temp_mass_diff = []
                            if i == 0 and j == 0:
                                if temp_mass[i][j] < old_with_0:
                                    return 0, 0, 0, temp_mass[i][j], diagonal_norma
                            elif i == 0 and j == 3:
                                for cur in [abs(temp_mass[i][j - 1] - temp_mass[i][j]),
                                            abs(temp_mass[i + 1][j] - temp_mass[i][j])]:
                                    if not cur == temp_mass[i][j]:
                                        temp_mass_diff.append(cur)
                            elif i == 3 and j == 0:
                                for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                            abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                    if not cur == temp_mass[i][j]:
                                        temp_mass_diff.append(cur)
                            elif i == 3 and j == 3:
                                if temp_mass[i][j] > old_with_0:
                                    return 3, 3, 0, temp_mass[i][j], diagonal_norma
                            elif i == 0:
                                for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                            abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                            abs(temp_mass[i][j - 1] - temp_mass[i][j])]:
                                    if not cur == temp_mass[i][j]:
                                        temp_mass_diff.append(cur)
                            elif j == 0:
                                for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                            abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                            abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                    if cur > 0:
                                        temp_mass_diff.append(cur)
                            elif i == 3:
                                for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                            abs(temp_mass[i - 1][j] - temp_mass[i][j]),
                                            abs(temp_mass[i][j - 1] - temp_mass[i][j])]:
                                    if not cur == temp_mass[i][j]:
                                        temp_mass_diff.append(cur)
                            elif j == 3:
                                for cur in [abs(temp_mass[i][j - 1] - temp_mass[i][j]),
                                            abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                            abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                    if not cur == temp_mass[i][j]:
                                        temp_mass_diff.append(cur)
                            if not ((i == 0 and j == 0 and len(temp_mass_diff) == 0) or (
                                    i == 3 and j == 3 and len(temp_mass_diff) == 0)):
                                if len(temp_mass_diff) == 0:
                                    temp_mass_diff.append(int(table_cards[k]))
                                temp_min = sum(temp_mass_diff) / len(temp_mass_diff)
                                if temp_min < min_difference:
                                    x, y, min_difference = i, j, temp_min
                                    temp_number = int(table_cards[k])
                                elif temp_min == min_difference:
                                    if old_with_0 == 0:
                                        x, y, min_difference = i, j, temp_min
                                        temp_number = int(table_cards[k])
                                if old_with_0 == 0 and temp_min < min_dif_with_0:
                                    x_with_0, y_with_0, min_dif_with_0 = i, j, temp_min
                                    temp_number_with_0 = int(table_cards[k])
    else:
        diagonal_norma = False
        wrong_odder = 0
        for a, b in zip(diagonal, diagonal[1:]):
            if a >= b:
                wrong_odder += 1
        for k in range(len(table_cards)):
            for i in range(4):
                temp_mass = copy.deepcopy(diagonal)
                temp_mass[i] = int(table_cards[k])
                temp_wrong_odder = 0
                for a, b in zip(temp_mass, temp_mass[1:]):
                    if a >= b:
                        temp_wrong_odder += 1
                if temp_wrong_odder < wrong_odder:
                    wrong_odder = temp_wrong_odder
                    x, y = i, i
                    min_difference, temp_number = int(table_cards[k]), int(table_cards[k])
    if min_dif_with_0 < 8 or sum([len(l) - l.count(0) for l in desk_comp]) > 11:
        return x_with_0, y_with_0, min_dif_with_0, temp_number_with_0, diagonal_norma
    return x, y, min_difference, temp_number, diagonal_norma


# поиск наилучшего хода бота картой из колоды
def find_best_move():
    x, y, min_difference = 0, 0, 20
    x_with_0, y_with_0, min_dif_with_0 = 0, 0, 20
    in_table = True
    cur_index = random.randint(0, len(cards) - 1)
    cur_number = cards.pop(cur_index)
    cur_step_number[0] = cur_number
    cards_choice.append(cur_number)
    label_num['text'] = 'Противник:' + str(cur_number)
    button_deck['text'] = 'Осталось ' + str(len(cards)) + ' карт(-а, -ы)'
    mass_for_range = [0, 1, 2, 3]
    root.tk_sleep(1)
    for k in range(2):
        if k == 1:
            mass_for_range.reverse()
        for i in mass_for_range:
            for j in mass_for_range:
                temp_mass = copy.deepcopy(desk_comp)
                old_number = temp_mass[i][j]
                temp_mass[i][j] = cur_number
                if check_wrong_completed(temp_mass):
                    dif = 0
                    last_num = temp_mass[i][0]
                    for d in range(j - 1, 0, -1):
                        if temp_mass[i][d] == 0:
                            dif += 1
                        else:
                            last_num = temp_mass[i][d]
                            break
                    dif_col = 0
                    last_num_col = temp_mass[0][j]
                    for d in range(i - 1, 0, -1):
                        if temp_mass[d][j] == 0:
                            dif_col += 1
                        else:
                            last_num_col = temp_mass[d][j]
                            break
                    if (dif < temp_mass[i][j] - last_num or dif == 0) and \
                            (dif_col < temp_mass[i][j] - last_num_col or dif_col == 0):
                        temp_mass_diff = []
                        if i == 0 and j == 0:
                            if cur_number < desk_comp[0][0]:
                                return 0, 0, False, 0
                            for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                        abs(temp_mass[i + 1][j] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif i == 0 and j == 3:
                            for cur in [abs(temp_mass[i][j - 1] - temp_mass[i][j]),
                                        abs(temp_mass[i + 1][j] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif i == 3 and j == 0:
                            for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                        abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif i == 3 and j == 3:
                            if cur_number > desk_comp[3][3]:
                                return 3, 3, False, 0
                            for cur in [abs(temp_mass[i][j - 1] - temp_mass[i][j]),
                                        abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif i == 0:
                            for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                        abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                        abs(temp_mass[i][j - 1] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif j == 0:
                            for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                        abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                        abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                if cur > 0:
                                    temp_mass_diff.append(cur)
                        elif i == 3:
                            for cur in [abs(temp_mass[i][j + 1] - temp_mass[i][j]),
                                        abs(temp_mass[i - 1][j] - temp_mass[i][j]),
                                        abs(temp_mass[i][j - 1] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        elif j == 3:
                            for cur in [abs(temp_mass[i][j - 1] - temp_mass[i][j]),
                                        abs(temp_mass[i + 1][j] - temp_mass[i][j]),
                                        abs(temp_mass[i - 1][j] - temp_mass[i][j])]:
                                if not cur == temp_mass[i][j]:
                                    temp_mass_diff.append(cur)
                        if not len(temp_mass_diff) == 0:
                            temp_min = sum(temp_mass_diff) / len(temp_mass_diff)
                            if temp_min < min_difference:
                                x, y, min_difference = i, j, temp_min
                                in_table = False
                            if temp_min < min_dif_with_0 and old_number == 0:
                                x_with_0, y_with_0, min_dif_with_0 = i, j, temp_min
                                in_table = False
    if min_dif_with_0 < 10 or min_dif_with_0 == min_difference or \
            (sum([len(l) - l.count(0) for l in desk_comp]) > 10 and min_dif_with_0 != 20):
        return x_with_0, y_with_0, in_table, min_dif_with_0
    return x, y, in_table, min_difference


# Ход компьютера
def move_comp():
    x, y = None, None
    if state_of_game['state'] == 'diagonal':
        cur_index = random.randint(0, len(cards) - 1)
        cur_number = cards.pop(cur_index)
        cur_step_number[0] = cur_number
        cards_choice.append(cur_number)
        label_num['text'] = 'Противник:' + str(cur_number)
        button_deck['text'] = 'Осталось ' + str(len(cards)) + ' карт(-а, -ы)'
        root.tk_sleep(1)
        if cur_step_number[0] < 10:
            for i in range(4):
                if desk_comp[i][i] == 0:
                    desk_comp[i][i] = cur_step_number[0]
                    chip_comp['prev'] = cur_step_number[0]
                    x, y = i, i
                    break
        else:
            for i in reversed(range(4)):
                if desk_comp[i][i] == 0:
                    desk_comp[i][i] = cur_step_number[0]
                    chip_comp['prev'] = cur_step_number[0]
                    x, y = i, i
                    break
        if state_of_game['step'] > 3:
            state_of_game['state'] = 'main'
    else:
        in_table = False
        x1, y1, min_difference1, temp_number1, diagonal_norma1 = find_best_move_with_cards_on_table()
        x2, y2, min_difference2, temp_number2, diagonal_norma2 = find_best_move_with_cards_on_table(True)
        if min_difference2 < min_difference1:
            x, y, min_difference, temp_number, diagonal_norma = x2, y2, min_difference2, temp_number2, diagonal_norma2
        else:
            x, y, min_difference, temp_number, diagonal_norma = x1, y1, min_difference1, temp_number1, diagonal_norma1
        cur_step_number[0] = temp_number

        if diagonal_norma:
            if min_difference <= 10:
                if not (temp_number == chip_comp['prev_in_table'] and desk_comp[x][y] == chip_comp['prev']):
                    table_cards.remove(str(temp_number))
                    label_table["text"] = 'На столе ' + ", ".join(table_cards)
                else:
                    if len(cards) > 0:
                        x, y, in_table, min_difference = find_best_move()
                    else:
                        table_cards.remove(str(temp_number))
                        label_table["text"] = 'На столе ' + ", ".join(table_cards)
            else:
                if len(cards) > 0:
                    x, y, in_table, min_difference = find_best_move()
                else:
                    table_cards.remove(str(temp_number))
                    label_table["text"] = 'На столе ' + ", ".join(table_cards)
        else:
            if not (min_difference == 20 and x == 0 and y == 0):
                if temp_number == chip_comp['prev_in_table'] and desk_comp[x][y] == chip_comp['prev']:
                    if len(cards) > 0:
                        x, y, in_table, min_difference = find_best_move()
                    else:
                        table_cards.remove(str(temp_number))
                        label_table["text"] = 'На столе ' + ", ".join(table_cards)

                else:
                    table_cards.remove(str(temp_number))
                    label_table["text"] = 'На столе ' + ", ".join(table_cards)
            else:
                if len(cards) > 0:
                    x, y, in_table, min_difference = find_best_move()
                else:
                    table_cards.remove(str(temp_number))
                    label_table["text"] = 'На столе ' + ", ".join(table_cards)
        label_num['text'] = 'Противник:' + str(cur_step_number[0])
        chip_comp['prev'] = cur_step_number[0]
        root.tk_sleep(1)
        if in_table:
            table_cards.append(str(cur_step_number[0]))
            chip_comp['prev_in_table'] = cur_step_number[0]
            label_table["text"] = 'На столе ' + ", ".join(table_cards)
            x, y = None, None
        else:
            if desk_comp[x][y] != 0:
                table_cards.append(str(desk_comp[x][y]))
                chip_comp['prev_in_table'] = desk_comp[x][y]
                label_table["text"] = 'На столе ' + ", ".join(table_cards)
            desk_comp[x][y] = cur_step_number[0]
    get_result()
    label_num['text'] = 'Ваш ход'
    state_of_game['block'] = False
    state_of_game['move'] = 'player'
    table_comp(x, y)


# расставление ячеек игрока
def table_player():
    mass = []
    myFont = font.Font(size=22)
    for i in range(4):
        for j in range(4):
            btn = tkinter.Button(root, text=desk_player[i][j], bg=color_player[i][j], width=3, height=1, font=myFont,
                                 command=lambda x=i, y=j, c=color_player[i][j]: change_number(x, y, c))
            btn.place(x=560 + 90 * j, y=300 + 90 * i)
            mass.append(btn)
    get_result()
    if state_of_game['move'] == 'comp':
        move_comp()
    return mass


# расставление ячеек бота
def table_comp(x=None, y=None):
    mass = []
    myFont = font.Font(size=22)
    for i in range(4):
        for j in range(4):
            if i == x and j == y:
                btn = tkinter.Button(text=desk_comp[i][j], bg='green', width=3, height=1, font=myFont)
            else:
                btn = tkinter.Button(root, text=desk_comp[i][j], bg='grey', width=3, height=1, font=myFont)
            btn.place(x=40 + 90 * j, y=300 + 90 * i)
            mass.append(btn)
    return mass


# выбор числа со стола игроком
def choice_in_table(x, top):
    cur_step_number[0] = int(x)
    table_cards.remove(x)
    label_table["text"] = 'На столе ' + ", ".join(table_cards)
    label_num['text'] = 'Ваше число: ' + str(cur_step_number[0])
    top.destroy()


# кнопка стол
# если число выбрано -- будет занесено на стол
# если нет -- будет предоставлен выбор числа со стола
def click_table():
    if state_of_game['state'] == 'main' and state_of_game['block'] is False:
        if not label_num['text'] == "Ваш ход":
            table_cards.append(str(cur_step_number[0]))
            label_table["text"] = 'На столе ' + ", ".join(table_cards)
            state_of_game['block'] = True
            state_of_game['move'] = 'comp'
            state_of_game['step'] += 1
            table_player()
        else:
            top_table = Toplevel(root)
            ttk.Label(top_table, text='выберите число').pack()
            for i in range(len(table_cards)):
                ttk.Button(top_table, text=table_cards[i],
                           command=lambda x=table_cards[i], top=top_table: choice_in_table(x, top)).pack()
            top_table.transient(root)
            top_table.grab_set()
            top_table.focus_set()
            top_table.wait_window()
            if not state_of_game['level_game'] == 0:
                change_color()
                table_player()


# main
tkinter.Misc.tk_sleep = tk_sleep  # Задержка во времени
root = tkinter.Tk()
root['bg'] = "lightgreen"
root.title("Lucky numbers")
root.geometry("900x750")

button_deck = tkinter.Button(root, text='Осталось ' + str(len(cards)) + ' карт(-а, -ы)', font=font.Font(size=10))
button_deck['command'] = click_func
combobox = ttk.Combobox(values=levels, state="readonly")
combobox.place(x=5, y=5)
button_start = tkinter.Button(root, text="Старт!", font=font.Font(size=12))
button_start['command'] = selected
label_table = ttk.Label(root, font=("Helvetica", 14), text="Стол пуст")
label_table.pack(ipadx=10, ipady=10)

label_num = ttk.Label(root, font=("Helvetica", 14), text="Выберите режим")
label_num.place(x=400, y=400)

button_table = tkinter.Button(root, text="Стол", font=font.Font(size=12))
button_table['command'] = click_table

tab_pl = table_player()
tab_c = table_comp()

button_deck.place(x=390, y=300)
button_start.place(x=200, y=5)
button_table.place(x=400, y=500)

root.mainloop()
