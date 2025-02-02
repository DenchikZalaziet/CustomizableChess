from board import Board
from pieces import *


def convert_user_x(user_x, size) -> int:  # превращение координаты x в координату массива
    x = abs(int(user_x) - size)
    return x


def convert_user_y(user_y) -> int:  # превращение координаты y в координату массива
    y = int(user_y) - 1
    return y


class Menu:
    board_type: int
    mode: int
    turns_enabled: bool
    mode_list: dict
    setup_list: dict

    def __init__(self, mode=0, board_type=1, turns_enabled=True) -> None:
        self.mode_list = {
            0: self.mode_menu,
            1: self.mode_play,
            2: self.mode_change_type,
            3: self.mode_change_size,
            4: self.mode_change_icon,
            5: self.mode_change_turns,
            6: self.mode_explode_square,
            7: self.mode_add_piece,
            8: self.mode_change_piece
        }
        self.setup_list = {
            0: self.setup_empty,
            1: self.setup_base,
            2: self.setup_bombs,
            3: self.setup_random
        }
        self.mode = mode
        self.board_type = board_type
        self.turns_enabled = turns_enabled
        self.board = Board(size=8, turns_enabled=turns_enabled)
        self.setup()

    def setup_empty(self) -> None:  # 0
        pass

    def setup_base(self) -> None:  # 1, традиционное расположение фигур на поле
        b = self.board
        size = b.size
        mid = size // 2
        mult = size // 8
        if size < 2:
            return
        for i in range(size):
            b.add(Pawn('b'), 1, i)
            b.add(Pawn('w'), size - 2, i)

        for i in range(mult):
            b.add(Rook('b'), 0, mid + 3 * mult - i + mult - 1)
            b.add(Rook('b'), 0, mid - 3 * mult - i - 1)
            b.add(Rook('w'), size - 1, mid + 3 * mult - i + mult - 1)
            b.add(Rook('w'), size - 1, mid - 3 * mult - i - 1)

        for i in range(mult):
            b.add(Knight('b'), 0, mid + 2 * mult - i + mult - 1)
            b.add(Knight('b'), 0, mid - 2 * mult - i - 1)
            b.add(Knight('w'), size - 1, mid + 2 * mult - i + mult - 1)
            b.add(Knight('w'), size - 1, mid - 2 * mult - i - 1)

        for i in range(mult):
            b.add(Bishop('b'), 0, mid + 1 * mult - i + mult - 1)
            b.add(Bishop('b'), 0, mid - 1 * mult - i - 1)
            b.add(Bishop('w'), size - 1, mid + 1 * mult - i + mult - 1)
            b.add(Bishop('w'), size - 1, mid - 1 * mult - i - 1)

        for i in range(mult):
            b.add(Queen('b'), 0, mid - 1 - i)
            b.add(Queen('w'), size - 1, mid - 1 - i)

        b.add(King('b'), 0, mid)
        b.add(King('w'), size - 1, mid)

    def setup_bombs(self) -> None:  # 2
        b = self.board
        size = b.size
        mid = size // 2
        mult = size // 8
        if size < 2:
            return
        for i in range(size):
            b.add(Bomb('b'), 1, i)
            b.add(Bomb('w'), size - 2, i)

        for i in range(mult):
            b.add(Rook('b'), 0, mid + 3 * mult - i + mult - 1)
            b.add(Rook('b'), 0, mid - 3 * mult - i - 1)
            b.add(Rook('w'), size - 1, mid + 3 * mult - i + mult - 1)
            b.add(Rook('w'), size - 1, mid - 3 * mult - i - 1)

        for i in range(mult):
            b.add(Knight('b'), 0, mid + 2 * mult - i + mult - 1)
            b.add(Knight('b'), 0, mid - 2 * mult - i - 1)
            b.add(Knight('w'), size - 1, mid + 2 * mult - i + mult - 1)
            b.add(Knight('w'), size - 1, mid - 2 * mult - i - 1)

        for i in range(mult):
            b.add(Bishop('b'), 0, mid + 1 * mult - i + mult - 1)
            b.add(Bishop('b'), 0, mid - 1 * mult - i - 1)
            b.add(Bishop('w'), size - 1, mid + 1 * mult - i + mult - 1)
            b.add(Bishop('w'), size - 1, mid - 1 * mult - i - 1)

        for i in range(mult):
            b.add(Queen('b'), 0, mid - 1 - i)
            b.add(Queen('w'), size - 1, mid - 1 - i)

        b.add(King('b'), 0, mid)
        b.add(King('w'), size - 1, mid)

    def setup_random(self) -> None:  # 3
        import random
        b = self.board
        size = b.size

        for i in range(size):
            new_piece = random.choice(list(Piece.piece_registry.values()))
            if new_piece == King:
                new_piece = Queen
            b.add(new_piece('b'), 1, i)
            b.add(new_piece('w'), size - 2, i)

        for i in range(size):
            new_piece = random.choice(list(Piece.piece_registry.values()))
            if new_piece == King:
                new_piece = Queen
            b.add(new_piece('b'), 0, i)
            b.add(new_piece('w'), size - 1, i)

        b.add(King('b'), 0, size // 2)
        b.add(King('w'), size - 1, size // 2)

    def setup(self) -> None:
        setup_mode = self.setup_list.get(self.board_type)
        if setup_mode:
            b = self.board
            b.white_king = True
            b.black_ling = True
            b.redraw()
            setup_mode()

    def check_mode(self) -> None:
        mode = self.mode_list.get(self.mode, self.mode_menu)
        mode()

    def mode_menu(self) -> None:  # 0
        print()
        print("Выберите режим:")
        print("1 - играть, 2 - выбрать тип, 3 - изменить размер, 4 - изменить иконку,")
        print("5 - включить/выключить ходы, 6 - взорвать клетку, 7 - добавить или заменить фигуру,")
        print("8 - изменить параметры фигуры")
        try:
            mode = int(input("--> "))
            self.mode = mode
        except ValueError:
            pass

    def mode_play(self) -> None:  # 1
        board = self.board
        board.draw()
        king = board.check_king()
        if king != -1:
            if king == 0:
                print("Победа черных")
            elif king == 1:
                print("Победа белых")
            elif king == 2:
                print("Ничья")
            self.mode = 0
            return
        if board.turns_enabled:
            turn = board.turn
            if turn == 'b':
                print("Ход черных")
            elif turn == 'w':
                print("Ход белых")

        try:
            user_input = input("Введите координаты x, y, target_x, target_y: ").split(',')
            if user_input[0] == "-":
                self.mode = 0
                return
            size = board.size
            x = convert_user_x(user_input[1], size)
            y = convert_user_y(user_input[0])
            target_x = convert_user_x(user_input[3], size)
            target_y = convert_user_y(user_input[2])
            res = board.move(x, y, target_x, target_y)
            if not res:
                print("# Неверный ход")
            elif res:
                print("# Ход удался")
        except (IndexError, ValueError):
            print("Неправильный формат ввода или входные данные")

    def mode_change_type(self) -> None:  # 2
        print("0 - пустое, 1 - обычное, 2 - бомбы, 3 - случайно")
        try:
            user_input = input("Введите тип поля: ")
            if user_input[0] == "-":
                return
            self.board_type = int(user_input)
            self.setup()
        except ValueError:
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 0
            print()

    def mode_change_size(self) -> None:  # 3
        try:
            user_input = input("Введите размер поля: ")
            if user_input[0] == "-":
                return
            size = int(user_input)
            if size < 0:
                size = 0
            self.board = Board(size=size, turns_enabled=self.turns_enabled)
            self.setup()
        except ValueError:
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 0
            print()

    def mode_change_icon(self) -> None:  # 4
        self.board.draw()
        try:
            user_input = input("1 - изменить одну фигуру, 2 - изменить все фигуры одного типа: ")
            if user_input[0] == "-":
                return
            if int(user_input) == 1:
                user_input = input("Введите координаты x, y и иконку: ").split(',')
                if user_input[0] == "-":
                    return
                x = convert_user_x(user_input[1], self.board.size)
                y = convert_user_y(user_input[0])
                new_icon = user_input[2]
                self.board.pieces[x][y].texture = new_icon
            elif int(user_input) == 2:
                user_input = input("Введите цвет, тип фигуры и иконку: ").split(',')
                if user_input[0] == "-":
                    return
                user_input[0] = user_input[0].replace(' ', '').lower()
                user_input[1] = user_input[1].replace(' ', '').lower()
                piece_color = user_input[0].lower().strip()
                piece_type = user_input[1].lower().strip()
                new_icon = user_input[2].strip()

                if piece_color in ["b", "black", "0"]:
                    piece_color = "b"
                elif piece_color in ["w", "white", "1"]:
                    piece_color = "w"
                elif piece_color in ["n", "none"]:
                    piece_color = "n"
                else:
                    raise ValueError

                Piece.texture_registry[piece_type][piece_color] = new_icon
            self.board.icon_size = Piece.get_texture_length()
        except (IndexError, KeyError, ValueError):
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 1
            print()

    def mode_change_turns(self) -> None:  # 5
        try:
            user_input = input("0 - выключить ходы, 1 - включить ходы: ")
            if user_input[0] == "-":
                return
            if user_input == "0":
                self.board.turns_enabled = False
            elif user_input == "1":
                self.board.turns_enabled = True
            else:
                raise ValueError
        except ValueError:
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 0
            print()

    def mode_explode_square(self) -> None:  # 6
        try:
            self.board.draw()
            user_input = input("Введите координаты x, y взрываемой клетки и радиус взрыва: ").replace(' ', '').lower().split(',')
            if user_input[0] == "-":
                self.mode = 0
                return
            size = self.board.size
            x = convert_user_x(user_input[1], size)
            y = convert_user_y(user_input[0])
            radius = max(int(user_input[2]), 0)

            bomb = Bomb('n')
            bomb.explosion_range = radius
            self.board.add(bomb, x, y)
            self.board.explode(x, y)
        except (IndexError, ValueError):
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 1
            print()

    def mode_add_piece(self) -> None:  # 7
        try:
            self.board.draw()
            user_input = input("Введите цвет, тип, координаты x, y: ").replace(' ', '').lower().split(',')
            if user_input[0] == "-":
                self.mode = 0
                return
            color = user_input[0]
            piece_type = user_input[1]
            x = convert_user_x(user_input[3], self.board.size)
            y = convert_user_y(user_input[2])
            piece = Piece.piece_registry.get(piece_type)
            if piece:
                self.board.add(piece(color), x, y)
            else:
                print(f"Не существует класс {piece_type}")
        except (IndexError, ValueError):
            print("Неправильный формат ввода или входные данные")
        finally:
            self.mode = 1
            print()

    def mode_change_piece(self) -> None:  # 8
        try:
            self.board.draw()

            user_input = input("1 - изменить одну фигуру, 2 - изменить все фигуры одного типа: ")
            if user_input[0] == "-":
                self.mode = 0
                return
            if user_input == '1':  # фигура
                user_input = input("Введите координаты x, y: ").replace(' ', '').lower().split(',')
                if user_input[0] == "-":
                    self.mode = 0
                    return
                x = convert_user_x(user_input[1], self.board.size)
                y = convert_user_y(user_input[0])
                piece = self.board.pieces[x][y]

                user_input = input("Введите название изменяемого параметра и новое значение: ").replace(' ', '').lower().split(',')
                param = str(user_input[0].replace(' ', '').lower().split(','))[2:-2]
                value = user_input[1].strip()
                if param == 'color':
                    if value in ["b", "black", "0"]:
                        value = "b"
                    elif value in ["w", "white", "1"]:
                        value = "w"
                    elif value in ["n", "none"]:
                        value = "n"
                    else:
                        raise ValueError

                piece.set_property(param, value)

            elif user_input == '2':  # класс
                user_input = input("Введите класс фигуры, название изменяемого параметра и новое значение: ").replace(' ', '').lower().split(',')
                piece_type = user_input[0].lower().strip()
                param = str(user_input[1].replace(' ', '').lower().split(','))[2:-2]
                value = user_input[2].strip()
                if param == 'color':
                    if value in ["b", "black", "0"]:
                        value = "b"
                    elif value in ["w", "white", "1"]:
                        value = "w"
                    elif value in ["n", "none"]:
                        value = "n"
                    else:
                        raise ValueError

                Piece.set_class_property(param, value, piece_type)

            else:
                raise ValueError
        except (ValueError, IndexError):
            print("Неправильный формат ввода или входные данные")
        finally:
            self.board.icon_size = Piece.get_texture_length()
            self.mode = 1
            print()
