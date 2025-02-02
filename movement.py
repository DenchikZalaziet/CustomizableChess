def check_collision(board: list, x: int, y: int, target_x: int, target_y: int, rang: int = -1, can_jump=False) -> int:
    # адекватно работает только для 8 направлений или со включенным прыжком
    # 0 - нельзя, 1 - можно, 2 - фигура на целевой клетке
    if rang != -1 and max(abs(target_x - x), abs(target_y - y)) > rang:
        return 0

    target_type = board[target_y][target_x].type

    if not (abs(target_x - x) == abs(target_y - y) or target_x == x or target_y == y):
        can_jump = True

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

            if board[y][x].type != 'empty' and (x != target_x or y != target_y):  # на текущей клете кто-то есть
                return 0

    if target_type == 'empty':  # на конечной клетке пусто
        return 1
    else:  # на конечной клетке кто-то есть
        return 2


class MovementType:
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        return False


class PawnMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        if piece.color == 'b' and target_y <= y:  # цель спереди или ссзади пешки
            return False
        elif piece.color == 'w' and target_y >= y:
            return False

        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_y].color

        if target_x == x and (res == 1 or res == 2 and piece.can_eat_own):  # ход в пределах одного столбца
            return True
        elif (res == 2 and abs(target_y - y) == 1 and abs(target_x - x) == 1 and  # ход по-диагонали
              (piece.can_eat_own or piece.color != target_color)):
            return True
        return False


class RookMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].color
        if not piece.can_eat_own and res == 2 and piece.color == target_color:
            return False

        if x == target_x or y == target_y:
            return True
        return False


class KnightMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].color
        if not piece.can_eat_own and res == 2 and piece.color == target_color:
            return False

        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return True
        return False


class BishopMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].color
        if not piece.can_eat_own and res == 2 and piece.color == target_color:
            return False

        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if dx == dy:
            return True
        return False


class QueenMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        target_color = board[target_y][target_x].color
        if not piece.can_eat_own and res == 2 and piece.color == target_color:
            return False
        dx = abs(x - target_x)
        dy = abs(y - target_y)
        if (x == target_x or y == target_y) or (dx == dy):
            return True
        return False


class KingMovement(MovementType):
    @staticmethod
    def validate(piece: any, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = check_collision(board, x, y, target_x, target_y, piece.range, piece.can_jump)
        if res == 0:
            return False
        elif res == 1:
            return True
        target_color = board[target_y][target_x].color

        if piece.can_eat_own or piece.color != target_color:
            return True
        return False
