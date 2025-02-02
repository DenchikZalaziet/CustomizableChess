def check_collision(board, x, y, target_x, target_y, rang=-1, can_jump=False) -> int:
    # адекватно работает только для 8 направлений или со включенным прыжком
    # 0 - нельзя, 1 - можно, 2 - фигура на целевой клетке
    if rang != -1 and max(abs(target_x - x), abs(target_y - y)) > rang:
        return 0

    target_type = board[target_y][target_x].get_type()

    if not can_jump:
        while x != target_x or y != target_y:
            if x < target_x:
                x += 1
            elif x > target_x:
                x -= 1
            if y < target_y:
                y += 1
            elif y > target_y:
                y -= 1

            if board[y][x].get_type() != 0 and (x != target_x or y != target_y):  # на текущей клете кто-то есть
                return 0

    if target_type == 0:  # на конечной клетке пусто
        return 1
    else:  # на конечной клетке кто-то есть
        return 2


class Piece:
    type = 0
    can_jump = False  # с ходами не по основным 8 направлениям лучше включать на 1
    can_eat_own = False
    can_explode = False
    rang = 0

    def __init__(self, color) -> None:
        self.color = color

    def set_range(self, change) -> None:
        self.rang = change

    def set_can_explode(self, new_value) -> None:
        self.can_explode = new_value

    def get_color(self) -> int:
        return self.color

    def get_type(self) -> int:
        return self.type

    def get_jump(self) -> bool:
        return self.can_jump

    def get_can_explode(self) -> bool:
        return self.can_explode

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        return False


class Pawn(Piece):
    type = 1
    rang = 2

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        if self.color == 0 and target_y <= y:  # цель спереди или ссзади пешки
            return False
        elif self.color == 1 and target_y >= y:
            return False

        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_y].get_color()

        if target_x == x and (res == 1 or res == 2 and self.can_eat_own):  # ход в пределах одного столбца
            return True
        elif (res == 2 and abs(target_y - y) == 1 and abs(target_x - x) == 1 and  # ход по-диагонали
              (self.can_eat_own or self.color != target_color)):
            return True
        return False


class Rook(Piece):
    type = 2
    rang = -1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].get_color()
        if not self.can_eat_own and res == 2 and self.color == target_color:
            return False

        if x == target_x or y == target_y:
            return True
        return False


class Knight(Piece):
    type = 3
    can_jump = True
    rang = -1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].get_color()
        if not self.can_eat_own and res == 2 and self.color == target_color:
            return False

        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return True
        return False


class Bishop(Piece):
    type = 4
    rang = -1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].get_color()
        if not self.can_eat_own and res == 2 and self.color == target_color:
            return False

        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if dx == dy:
            return True
        return False


class Queen(Piece):
    type = 5
    rang = -1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].get_color()
        if not self.can_eat_own and res == 2 and self.color == target_color:
            return False
        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if (x == target_x or y == target_y) or (dx == dy):
            return True
        return False


class King(Piece):
    type = 6
    rang = 1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        if res == 0:
            return False
        elif res == 1:
            return True
        target_color = board[target_y][target_x].get_color()

        if self.can_eat_own or self.color != target_color:
            return True
        return False


class Bomb(Piece):
    type = 7
    can_eat_own = True
    can_explode = True
    rang = 1

    def check_move(self, board, x, y, target_x, target_y) -> bool:
        res = check_collision(board, x, y, target_x, target_y, self.rang, self.can_jump)
        target_color = board[target_y][target_x].get_color()
        if res == 0:
            return False
        elif self.can_eat_own or self.color != target_color or res == 1:
            return True
        return False

