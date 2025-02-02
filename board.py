from pieces import Piece, Empty


def draw_marker_x(icon_size=0, size=8) -> None:
    for _ in range(len(str(size)) + 2):  # отступ в начале последней строки
        print(end=' ')
    for i in range(1, size + 1):  # столбцы
        index_x = str(i)
        while len(index_x) < len(str(size)) or len(index_x) < icon_size:
            index_x += ' '
        print(index_x, end=' ')
    print()


class Board:
    size: int
    icon_size: int
    pieces: list
    turn: str
    turns_enabled: bool

    def __init__(self, size=8, turn='w', turns_enabled=True) -> None:
        pieces = [[Empty('b') for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if (i + j) % 2 == 0:
                    pieces[i][j] = Empty('w')
        self.size = size
        self.icon_size = Piece.get_texture_length()
        self.pieces = pieces
        self.turn = turn
        self.turns_enabled = turns_enabled

    def fill_square(self, x: int, y: int) -> None:
        if (x + y) % 2 == 0:  # очистка клетки после взрыва
            self.pieces[x][y] = Empty('w')
        else:
            self.pieces[x][y] = Empty('b')

    def add(self, piece: Piece, x: int, y: int) -> None:
        self.pieces[x][y] = piece

    def remove(self, target_x: int, target_y: int) -> None:
        if (target_x + target_y) % 2 == 0:
            self.pieces[target_x][target_y] = Empty('w')
        else:
            self.pieces[target_x][target_y] = Empty('b')

    def draw(self) -> None:
        size = self.size
        icon_size = self.icon_size

        draw_marker_x(icon_size, size)

        for i in range(size):
            index_y = str(abs(i - size))  # индекс строки
            while len(index_y) < len(str(size)):
                index_y += ' '
            print(index_y, ": ", sep='', end='')

            for j in range(size):  # фигуры
                try:
                    icon = self.pieces[i][j].texture
                except IndexError:
                    icon = "None"
                    print("Невозможно отобразить фигуру")
                while len(icon) < len(str(size)) or len(icon) < icon_size:
                    icon += ' '
                print(icon, end=' ')

            print(":", index_y, sep='')
        draw_marker_x(icon_size, size)
        print()

    def redraw(self, turn='w') -> None:
        pieces = [[Empty('b') for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 0:
                    pieces[i][j] = Empty('w')
        self.pieces = pieces
        self.turn = turn

    def clear(self) -> None:
        self.pieces = []
        self.turn = 'w'

    def check_move(self, x: int, y: int, target_x: int, target_y: int) -> bool:
        if target_x > self.size - 1 or target_x < 0 or target_y > self.size - 1 or target_y < 0:
            print("Ход за пределы поля")
            return False
        return self.pieces[x][y].check_move(self.pieces, y, x, target_y, target_x)

    def check_king(self) -> int:
        black_king = False
        white_king = False
        for row in self.pieces:
            for piece in row:
                if piece.type == 'king':
                    if piece.color == 'b':
                        black_king = True
                    elif piece.color == 'w':
                        white_king = True
        if black_king and white_king:
            return -1
        elif black_king:
            return 0
        elif white_king:
            return 1
        else:
            return 2

    def move(self, x: int, y: int, target_x: int, target_y: int,
             remove_acting_piece=True, change_target_piece=True, change_turns=True) -> bool:
        if self.pieces[x][y].color != 'n':
            if change_turns and self.turns_enabled and self.pieces[x][y].color != self.turn:
                return False

        if not self.check_move(x, y, target_x, target_y):
            return False
        else:
            moving_piece = self.pieces[x][y]
            target_piece = self.pieces[target_x][target_y]

            if change_target_piece:
                self.pieces[target_x][target_y] = self.pieces[x][y]

            if remove_acting_piece:
                self.fill_square(x, y)

            if (target_piece.type != 'empty' and
                    (moving_piece.can_explode or target_piece.can_explode)):  # съедена или взорвалась бомба
                self.explode(target_x, target_y)

            if change_turns and self.turns_enabled:
                if self.turn == 'w':  # смена хода
                    self.turn = 'b'
                elif self.turn == 'b':
                    self.turn = 'w'
            return True

    def explode(self, x: int, y: int) -> None:
        bomb = self.pieces[x][y]
        explosion_range = self.pieces[x][y].explosion_range
        self.pieces[x][y].can_explode = False
        for i in range(x - explosion_range, x + 1 + explosion_range):
            for j in range(y - explosion_range, y + 1 + explosion_range):
                if 0 <= i < self.size and 0 <= j < self.size:
                    if self.pieces[i][j].can_explode:
                        self.move(x, y, i, j, change_target_piece=True, remove_acting_piece=True, change_turns=False)
                        self.pieces[x][y] = bomb
                    elif i != x or j != y:
                        self.fill_square(i, j)
        self.fill_square(x, y)
