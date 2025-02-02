from pieces import Piece


def draw_marker_x(icon_size=0, size=8) -> None:
    for _ in range(len(str(size)) + 2):  # отступ в начале последней строки
        print(end=' ')
    for i in range(1, size + 1):  # столбцы
        index_x = str(i)
        while len(index_x) < len(str(size)) or len(index_x) < icon_size:
            index_x += ' '
        print(index_x, end=' ')
    print()


def calculate_icon_size(icons) -> int:
    number_of_pieces = len(icons[0])
    for i in icons:
        if len(i) != number_of_pieces:
            raise Exception("У фигуры нет иконки одного из цветов")
    icon_size = 0
    for color in icons:
        for item in color:
            if len(item) > icon_size:
                icon_size = len(item)
    return icon_size


class Board:
    size = 0
    turns_enabled = True
    turn = 1
    icons = [["  ", "Bp", "Br", "Bk", "Bb", "Bq", "BK", "Bmb"],  # черные
             ["##", "Wp", "Wr", "Wk", "Wb", "Wq", "WK", "Wmb"]]  # белые
    white_king = True
    black_ling = True

    def __init__(self, new_size=8, turns_enabled=True) -> None:
        pieces = [[Piece(0) for _ in range(new_size)] for _ in range(new_size)]
        for i in range(new_size):
            for j in range(new_size):
                if (i + j) % 2 == 0:
                    pieces[i][j] = Piece(1)
        self.size = new_size
        self.pieces = pieces
        self.turns_enabled = turns_enabled
        self.icon_size = calculate_icon_size(self.icons)

    def fill_square(self, x, y, king_check=False) -> None:
        piece = self.pieces[x][y]
        if king_check and piece.get_type() == 6:
            if piece.get_color() == 0:
                self.black_ling = False
            elif piece.get_color() == 1:
                self.white_king = False

        if (x + y) % 2 == 0:  # очистка клетки после взрыва
            self.pieces[x][y] = Piece(1)
        else:
            self.pieces[x][y] = Piece(0)

    def add(self, piece: Piece, target_x, target_y) -> None:
        self.pieces[target_x][target_y] = piece

    def remove(self, target_x, target_y) -> None:
        if (target_x + target_y) % 2 == 0:
            self.pieces[target_x][target_y] = Piece(1)
        else:
            self.pieces[target_x][target_y] = Piece(0)

    def set_turns_enabled(self, new_turns_enabled) -> None:
        self.turns_enabled = new_turns_enabled

    def set_kings(self, black=True, white=True) -> None:
        self.black_ling = black
        self.white_king = white

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
                piece_type = self.pieces[i][j].get_type()
                piece_color = self.pieces[i][j].get_color()
                try:
                    icon = self.icons[piece_color][piece_type]
                except IndexError:
                    raise Exception("У фигуры нет иконки")
                while len(icon) < len(str(size)) or len(icon) < icon_size:
                    icon += ' '
                print(icon, end=' ')

            print(":", index_y, sep='')
        draw_marker_x(icon_size, size)
        print()

    def redraw(self) -> None:
        pieces = [[Piece(0) for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 0:
                    pieces[i][j] = Piece(1)
        self.pieces = pieces
        self.turn = 1

    def clear(self) -> None:
        self.pieces = []
        self.turn = 1

    def change_icon(self, piece_color, piece_type, new_icon) -> None:
        self.icons[piece_color][piece_type] = new_icon
        self.icon_size = calculate_icon_size(self.icons)

    def check_move(self, x, y, target_x, target_y) -> bool:
        if target_x > self.size - 1 or target_x < 0 or target_y > self.size - 1 or target_y < 0:
            print("Ход за пределы поля")
            return False
        return self.pieces[x][y].check_move(self.pieces, y, x, target_y, target_x)

    def check_king(self) -> int:
        if not self.white_king and not self.black_ling:
            return 2
        elif not self.black_ling:
            return 0
        elif not self.white_king:
            return 1
        else:
            return -1

    def move(self, x, y, target_x, target_y, remove_acting_piece=True, change_target_piece=True, change_turns=True) -> bool:
        if change_turns and self.turns_enabled and self.pieces[x][y].get_color() != self.turn:
            return False
        if not self.check_move(x, y, target_x, target_y):
            return False
        else:
            moving_piece = self.pieces[x][y]
            target_piece = self.pieces[target_x][target_y]

            if target_piece.get_type() == 6:
                if target_piece.get_color() == 0:
                    self.black_ling = False
                elif target_piece.get_color() == 1:
                    self.white_king = False

            if change_target_piece:
                self.pieces[target_x][target_y] = self.pieces[x][y]

            if remove_acting_piece:
                self.fill_square(x, y)

            if (target_piece.get_type() != 0 and
                    (moving_piece.get_can_explode() or target_piece.get_can_explode())):  # съедена или взорвалась бомба
                self.explode(target_x, target_y)

            if change_turns and self.turns_enabled:
                if self.turn == 1:  # смена хода
                    self.turn = 0
                elif self.turn == 0:
                    self.turn = 1
            return True

    def get_pieces(self):
        return self.pieces

    def get_turns_enabled(self):
        return self.turns_enabled

    def get_size(self) -> int:
        return self.size

    def get_icon_size(self) -> int:
        return self.icon_size

    def get_turn(self) -> int:
        return self.turn

    def explode(self, x, y) -> None:
        bomb = self.pieces[x][y]
        self.pieces[x][y].set_can_explode(False)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < self.size and 0 <= j < self.size:
                    if self.pieces[i][j].get_can_explode():
                        self.move(x, y, i, j, change_target_piece=True, remove_acting_piece=True, change_turns=False)
                        self.pieces[x][y] = bomb
                    elif i != x or j != y:
                        self.fill_square(i, j, king_check=True)
        self.fill_square(x, y)
