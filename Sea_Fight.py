class BoardOutException(Exception):  # Исключение контролирующее выход за доску
    pass
class ShotDotException(Exception):    # Попытка выстрелить в 'прострелянную' точку
    pass
class ShotShipException(Exception):   # Попадание в корабль
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length, nose, direction, hp):
        self.length = length
        self.nose = nose
        #direction принимает значения True или False
        self.direction = direction
        self.hp = hp
        
    def dots(self):
        d = [self.nose]
        if self.direction:
            for i in range(1, self.length):
                d.append(Dot(self.nose.x, self.nose.y+i))
            return d
        else:
            for i in range(1, self.length):
                d.append(Dot(self.nose.x + i, self.nose.y))
            return d
#Контур включает и точки самого корабля, но это неважно
    @property
    def contour(self):
        cont = []
        for i in self.dots():
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if all([i.x + j > 0, i.x + j  < 7, i.y + k > 0, i.y + k < 7]):
                        cont.append(Dot(i.x + j, i.y + k))
        #cont = list(set(cont))
        return cont

class Board:
    def __init__(self, board_, name = None, hid = False):
        self.board = board_
        self.hid = hid
        self.list_ship = [] #Список кораблей на доске
        self.list_contour = [] #Список точек всех контуров на доске
        self.list_dots_ship = [] #Список точек всех кораблей на доске
        self.list_shot_dots = []  #Список "прострелянных" точек доски
        self.name = name # имя доски

    def set_name(self, name):
        self.name = name
# метод генерирующий пустую доску
    @staticmethod
    def initial_board():
        board = [['~' for j in range(7)] for j in range(7)]
        board[0] = [' ', 1, 2, 3, 4, 5, 6]
        for i in range(1, 7):
            board[i][0] = i
        return board
# метод генерирующий список всех координат доски
    @staticmethod
    def list_position_board():
        p_b_ = []
        for i in range(1,7):
            for j in range(1,7):
                p_b_.append((i,j))
        return p_b_
# метод, рисующий доску
    def print_board(self):
        if not self.name is None:
            print(f'{self.name}')
        for i in self.board:
            for j in i:
                if j != '~':
                    print(j, end = ' | ')
                else:
                    print("\033[1m\033[34m{}\033[0m".format(j), end = ' | ')
            print()
# метод, рисующий две доски рядом
    def print_two_board(self, other):
        print(f'{self.name}', end=' ')
        print('                     ',f'{other.name}')
        print()
        for i,j in zip(self.board, other.board):
            for k in i:
                if k == '~':
                    print("\033[1m\033[34m{}\033[0m".format(k), end=' | ')
                elif k == 'X':
                    print("\033[1m\033[31m{}\033[0m".format(k), end=' | ')
                elif k=='T':
                    print("\033[1m\033[32m{}\033[0m".format(k), end=' | ')
                else:
                    print(k, end=' | ')
            print(' \t ', end = ' ')
            for l in j:
                if l == '~':
                    print("\033[1m\033[34m{}\033[0m".format(l), end=' | ')
                elif l == 'X':
                    print("\033[1m\033[31m{}\033[0m".format(l), end=' | ')
                elif l=='T':
                    print("\033[1m\033[32m{}\033[0m".format(l), end=' | ')
                else:
                    print(l, end=' | ')
            print()

    def add_ship(self, ship):
        if not self.hid:
            for i in ship.dots():
                self.board[i.y][i.x] = '■'
        self.list_ship.append(ship)
        for i in ship.contour:
            self.list_contour.append(i)
        for i in ship.dots():
            self.list_dots_ship.append(i)
    #количество живых кораблей
    @property
    def quantity_ships(self):
        return len(self.list_ship)

    def shot(self, dot):
        if dot in self.list_shot_dots:
            raise ShotDotException()
        elif any([dot.x < 1, dot.x > 6, dot.y < 1, dot.y > 6]):
            raise BoardOutException()
        elif dot in self.list_dots_ship:
            self.board[dot.y][dot.x] = 'X'
            self.list_shot_dots.append(dot)
            for i in self.list_ship:
                if dot in i.dots():
                    i.hp -= 1
                    break
            raise ShotShipException()
        else:
            self.board[dot.y][dot.x] = 'T'
            self.list_shot_dots.append(dot)

class Player:
    def ask(self):
        pass
    def move(self, board):
        import time
        try:
            p = self.ask()
            board.shot(p)
        except ValueError:
            print()
            print('Некорректный ввод')
            print()
            return True
        except BoardOutException:
            print()
            print('Выстрел за пределы поля! Попробуйте еще раз')
            print()
            return True
        except ShotDotException:
            print()
            print('Нет смысла стрелять в эту точку!')
            print()
            return True
        except ShotShipException:
            for i in range(1, 5):
                print('Снаряд летит', '.' * i, end='\r', flush=True)
                time.sleep(0.42)
            print(end='\r', flush=True)
            print()
            print('Противник ранен!')
            print()
            return True
        else:
            for i in range(1, 5):
                print('Снаряд летит', '.' * i, end='\r', flush=True)
                time.sleep(0.42)
            print(end='\r', flush=True)
            print()
            print('Промах! Теперь ход противника')
            print()
            return False


class User(Player):
    def ask(self):
        y = input('Куда стреляем (строка)?: ')
        x = input('Куда стреляем (столбец)?: ')
        if x.isdigit() and y.isdigit():
            return Dot(int(x), int(y))
        else:
            raise ValueError()
# метод, проверяющий уничтожен ли корабль
    def kill_ship(self, board_):
        for ship in board_.list_ship:
            if ship.hp == 0:
                for dot in ship.contour:
                    board_.board[dot.y][dot.x] = 'T'
                    board_.list_shot_dots.append(dot)
                for dot in ship.dots():
                    board_.board[dot.y][dot.x] = 'X'
                board_.list_ship.remove(ship)
                print()
                print('Вы уничтожили корабль противника!')
                print()
                break
# большой и неприятный метод, генерирующий доску игрока
    @staticmethod
    def generation_board():
        board1 = Board(Board.initial_board())
        initial_set = [3,2,2,1,1,1,1] # начальный набор кораблей
        while board1.quantity_ships < 7:
            try:
                free_position = False
                for i, j in Board.list_position_board():
                    if not Dot(j,i) in board1.list_contour:
                        free_position = True
                if not free_position:
                    print('Не осталось места для корабля, давайте начнем сначала')
                    board1 = Board(Board.initial_board())
                    initial_set = [3, 2, 2, 1, 1, 1, 1]

                print(f'Поставьте корабль размера {initial_set[0]}')
                if initial_set[0] > 1:
                    list_ = [initial_set[0], input('Строка положения носа корабля: '), input('Столбец положения носа корабля: '), input('Его положение (введите "v" - вертикально или "g" - горизонтально, без кавычек): ')]
                else:
                    list_ = [initial_set[0], input('Строка положения корабля: '), input('Столбец положения корабля: '), 'v']

                if (not list_[1].isdigit()) or (not list_[2].isdigit()) or (not list_[3].isalpha()):
                    raise TypeError()

                if (not (list_[3] == 'v')) and (not (list_[3] == 'g')):
                    raise TypeError()

                point = Dot(int(list_[2]), int(list_[1]))
                direct = list_[3]
                direct = True if (direct == 'v') else False
                ship = Ship(list_[0], point, direct, int(list_[0]))
                for i in ship.dots():
                    if any([i.x < 1, i.x > 6, i.y < 1, i.y > 6]):
                        raise BoardOutException()
                    if i in board1.list_contour:
                        raise ValueError()
            except BoardOutException:
                print()
                print('Ваш корабль выходит за пределы поля!')
                print()
            except ValueError:
                print()
                print('Вы ставите корабли слишком близко!')
                print()
                #continue
            except TypeError:
                print()
                print('Некорректный ввод')
                print()
            else:
                board1.add_ship(ship)
                board1.print_board()
                initial_set.pop(0)
        return board1

class AI(Player):
    def ask(self):
        import random
        random_number = random.randint(0, 35)
        rand_coord = Board.list_position_board()[random_number]
        point = Dot(rand_coord[1], rand_coord[0])
        return point
#Далее функция, которая добивает корабли
    def finish_ship(self, ship, board):
        import random
        V = [(1,0), (-1,0), (0,1), (0, -1)]
        random_number = random.randint(0, 3)
        random_number1 = random.randint(0, 1)
        if len(ship.dots()) - ship.hp == 1:
            for shot in board.list_shot_dots:
                if shot in ship.dots():
                    x = shot.x
                    y = shot.y
                    break
            point = Dot(x + V[random_number][0],y + V[random_number][1])
            return point
        if len(ship.dots()) - ship.hp > 1:
            for shot in board.list_shot_dots:
                if shot in ship.dots():
                    x1 = shot.x
                    y1 = shot.y
            for shot in board.list_shot_dots:
                if (shot in ship.dots()) and (shot != Dot(x1, y1)):
                    x2 = shot.x
                    y2 = shot.y
            if x1 == x2:
                x3 = x1
                if random_number1 == 0:
                    y3 = min(y1,y2) - 1
                else:
                    y3 = max(y1,y2) + 1
            else:
                y3 = y1
                if random_number1 == 0:
                    x3 = min(x1, x2) - 1
                else:
                    x3 = max(x1, x2) + 1
            point = Dot(x3,y3)
            return point

    def move(self, board):
        import time
        p = self.ask()
        # проверим есть ли недобитый корабль
        for ship in board.list_ship:
            if 0 < ship.hp < len(ship.dots()):
                p = self.finish_ship(ship, board)
                break
        try:
            board.shot(p)
        except BoardOutException:
            return None
        except ShotDotException:
            return None
        except ShotShipException:
            for i in range(1, 7):
                print('Снаряд летит', '.' * i, end='\r', flush=True)
                time.sleep(0.42)
            print(end='\r', flush=True)
            print()
            print('Вы ранены!')
            print()
            return True
        else:
            for i in range(1, 7):
                print('Снаряд летит', '.' * i, end='\r', flush=True)
                time.sleep(0.42)
            print(end = '\r', flush = True)
            print('Противник промахнулся')
            return False

    def kill_ship(self, board_):
        for ship in board_.list_ship:
            if ship.hp == 0:
                for dot in ship.contour:
                    board_.board[dot.y][dot.x] = 'T'
                    board_.list_shot_dots.append(dot)
                for dot in ship.dots():
                    board_.board[dot.y][dot.x] = 'X'
                board_.list_ship.remove(ship)
                print()
                print('Ваш корабль уничтожен')
                print()
                break
# метод, генерирующий доску ИИ
    @staticmethod
    def generation_board():
        board2 = Board(Board.initial_board(), hid = True)
        initial_set = [3, 2, 2, 1, 1, 1, 1]
        import random
        while board2.quantity_ships < 7:
            free_position = False
            for i, j in Board.list_position_board():
                if not Dot(j, i) in board2.list_contour:
                    free_position = True
            if not free_position:
                board2 = Board(Board.initial_board(), hid = True)
                initial_set = [3, 2, 2, 1, 1, 1, 1]
            random_number = random.randint(0, 35)
            direct = random.randint(0, 1)
            rand_coord = Board.list_position_board()[random_number]
            point = Dot(rand_coord[1], rand_coord[0])
            ship = Ship(initial_set[0], point, direct, initial_set[0])
            try:
                for i in ship.dots():
                    if any([i.x < 1, i.x > 6, i.y < 1, i.y > 6]):
                        raise ValueError()
                    if i in board2.list_contour:
                        raise ValueError()
            except ValueError:
                pass
            else:
                board2.add_ship(ship)
                initial_set.pop(0)
        return  board2

class Game:
    def greet(self):
        print('Здравствуйте! Спасибо за запуск игры!')
        print('''
         Хотелось бы немного рассказать про формат ввода. Далее вам будет предложено расставить корабли на свою доску.
         Палуба корабля идет вниз или вправо от носа в зависимости от выбора направления. 
         Если хотите расположить корабль по вертикали введите в поле выбора направления 'v'(без ковычек), иначе 'g' (горизонтально). 
         Ввод координат носа корабля, а также координат выстрела происходит построчно, сначала строка, потом столбец.
         Удачной игры!)''')
        Board(Board.initial_board()).print_board()
        input('Нажмите Enter, чтобы продолжить')

    def loop(self):
        u =User()
        a = AI()
        #User.generation_board()
        print()
        #AI.generation_board()
        b1 = User.generation_board()
        print()
        b2 = AI.generation_board()
        b1.set_name('Ваша доска')
        b2.set_name('Доска противника')
        b2.print_board()
        while b1.quantity_ships > 0 and b2.quantity_ships > 0:
            user_shot = True
            while user_shot:
                user_shot = u.move(b2)
                u.kill_ship(b2)

               # for i in range(1,7):
                   # print('Снаряд летит', '.' * i, end = '\r', flush = True)
                   # time.sleep(0.37)

                b1.print_two_board(b2)
                if b2.quantity_ships == 0:
                    print('Вы победили! Весь флот противника разгромлен!')
                    break

            if b2.quantity_ships == 0:
                print('Поздравляю!')
                break
            ai_shot = True
            print()
            while ai_shot:
                ai_shot = a.move(b1)
                a.kill_ship(b1)
                if ai_shot is None:
                    ai_shot = True
                    continue
                print()
                b1.print_two_board(b2)
                print()
                if b1.quantity_ships == 0:
                    print('Вы проиграли(')
                    break
                
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
