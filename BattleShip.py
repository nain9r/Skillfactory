from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):

    def __str__(self):
        return 'Вы пытаетесь ввести координаты, выходящие за поле!'


class BoardUsedException(BoardException):

    def __str__(self):
        return 'По данным координатам уже либо был произведен выстрел, либо не может располагаться корабль!'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, z):
        return self.x == z.x and self.y == z.y


class Ship:

    def __init__(self, bow, length, orient):
        self.length = length
        self.bow = bow
        self.orient = orient
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orient == 0:
                current_x += i

            elif self.orient == 1:
                current_y += i

            ship_dots.append(Dot(current_x, current_y))

        return ship_dots


class Board:
    def __init__(self, hid=False, size=10):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [['O'] * size for _ in range(size)]
        self.taken = []
        self.ships = []

    def add_ship(self, ship):
        for i in ship.dots:
            if self.out(i) or i in self.taken:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.field[i.x][i.y] = '■'
            self.taken.append(i)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, var=False):
        close = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for dx, dy in close:
                current = Dot(i.x + dx, i.y + dy)
                if not (self.out(current)) and current not in self.taken:
                    if var:
                        self.field[current.x][current.y] = "."
                    self.taken.append(current)

    def __str__(self):
        b_show = '   \u03320  \u03321  \u03322  \u03323  \u03324  \u03325  \u03326  \u03327  \u03328  \u03329'
        for i, row in enumerate(self.field):
            b_show += f'\n{i}| ' + '  '.join(row) + ' '
        if self.hid:
            b_show = b_show.replace('■', 'O')
        return b_show

    def out(self, a):
        return not ((0 <= a.x < self.size) and (0 <= a.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.taken:
            raise BoardUsedException()

        self.taken.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, var=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.taken = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 9), randint(0, 9))
        print(f'Ход компьютера: {d.x} {d.y}')
        return d


class User(Player):
    def ask(self):
        while True:
            move_coord = input('Ваш ход: ').split()

            if len(move_coord) != 2:
                print('Введите 2 координаты!')
                continue

            x, y = move_coord

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа!')
                continue

            x, y = int(x), int(y)

            return Dot(x, y)


class Game:
    def __init__(self, size=10):
        self.size = size
        player = self.random_board()
        machine = self.random_board()
        machine.hid = True

        self.ai = AI(machine, player)
        self.us = User(player, machine)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        ship_length = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in ship_length:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print('Добро пожаловать в игру "Морской бой"! '
              'Введите координаты цифрами в формате x y, где x - номер строки, y - номер столбца.')

    def loop(self):
        n = 0
        while True:
            print('\nКарта игрока:\n')
            print(self.us.board)
            print('\nКарта компьютера:\n')
            print(self.ai.board)
            if n % 2 == 0:
                print('\nХодит игрок!')
                repeat = self.us.move()
            else:
                print('\nХодит компьютер!')
                repeat = self.ai.move()
            if repeat:
                n -= 1

            if self.ai.board.count == 10:
                print('\nИгрок выиграл!')
                break

            if self.us.board.count == 10:
                print('\nКомпьютер выиграл!')
                break
            n += 1

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
