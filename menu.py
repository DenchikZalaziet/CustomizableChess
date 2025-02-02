from board import Board
from pieces import Pawn, Knight, Bishop, Rook, Queen, King, Bomb


def convert_user_x(user_x, size) -> int:  # превращение координаты x в координату массива
    x = abs(int(user_x) - size)
    return x


def convert_user_y(user_y) -> int:  # превращение координаты y в координату массива
    y = int(user_y) - 1
    return y


class Menu:
    board_type = 1
    mode = 0
    turns_enabled = True

    def __init__(self) -> None:
        self.board = Board(new_size=8, turns_enabled=self.turns_enabled)
        self.setup()

    def setup(self) -> None:
        board_type = self.board_type
        b = self.board
        b.set_kings()
        if board_type == 0:
            b.redraw()
        elif board_type == 1:
            b.redraw()
            self.setup_base()
        elif board_type == 2:
            b.redraw()
            self.setup_bombs()

    def setup_base(self) -> None:  # традиционное расположение фигур на поле
        b = self.board
        size = b.get_size()
        mid = size // 2
        mult = size // 8
        if size < 2:
            return
        for i in range(size):
            b.add(Pawn(0), 1, i)
            b.add(Pawn(1), size - 2, i)

        for i in range(mult):
            b.add(Rook(0), 0, mid + 3 * mult - i + mult - 1)
            b.add(Rook(0), 0, mid - 3 * mult - i - 1)
            b.add(Rook(1), size - 1, mid + 3 * mult - i + mult - 1)
            b.add(Rook(1), size - 1, mid - 3 * mult - i - 1)

        for i in range(mult):
            b.add(Knight(0), 0, mid + 2 * mult - i + mult - 1)
            b.add(Knight(0), 0, mid - 2 * mult - i - 1)
            b.add(Knight(1), size - 1, mid + 2 * mult - i + mult - 1)
            b.add(Knight(1), size - 1, mid - 2 * mult - i - 1)

        for i in range(mult):
            b.add(Bishop(0), 0, mid + 1 * mult - i + mult - 1)
            b.add(Bishop(0), 0, mid - 1 * mult - i - 1)
            b.add(Bishop(1), size - 1, mid + 1 * mult - i + mult - 1)
            b.add(Bishop(1), size - 1, mid - 1 * mult - i - 1)

        for i in range(mult):
            b.add(Queen(0), 0, mid - 1 - i)
            b.add(Queen(1), size - 1, mid - 1 - i)

        b.add(King(0), 0, mid)
        b.add(King(1), size - 1, mid)

    def setup_bombs(self) -> None:
        b = self.board
        size = b.get_size()
        mid = size // 2
        mult = size // 8
        if size < 2:
            return
        for i in range(size):
            b.add(Bomb(0), 1, i)
            b.add(Bomb(1), size - 2, i)

        for i in range(mult):
            b.add(Rook(0), 0, mid + 3 * mult - i + mult - 1)
            b.add(Rook(0), 0, mid - 3 * mult - i - 1)
            b.add(Rook(1), size - 1, mid + 3 * mult - i + mult - 1)
            b.add(Rook(1), size - 1, mid - 3 * mult - i - 1)

        for i in range(mult):
            b.add(Knight(0), 0, mid + 2 * mult - i + mult - 1)
            b.add(Knight(0), 0, mid - 2 * mult - i - 1)
            b.add(Knight(1), size - 1, mid + 2 * mult - i + mult - 1)
            b.add(Knight(1), size - 1, mid - 2 * mult - i - 1)

        for i in range(mult):
            b.add(Bishop(0), 0, mid + 1 * mult - i + mult - 1)
            b.add(Bishop(0), 0, mid - 1 * mult - i - 1)
            b.add(Bishop(1), size - 1, mid + 1 * mult - i + mult - 1)
            b.add(Bishop(1), size - 1, mid - 1 * mult - i - 1)

        for i in range(mult):
            b.add(Queen(0), 0, mid - 1 - i)
            b.add(Queen(1), size - 1, mid - 1 - i)

        b.add(King(0), 0, mid)
        b.add(King(1), size - 1, mid)

    def check_mode(self) -> None:
        mode = self.mode
        if mode == 0:
            self.mode_menu()
        elif mode == 1:
            self.mode_play()
        elif mode == 2:
            self.mode_change_type()
        elif mode == 3:
            self.mode_change_size()
        elif mode == 4:
            self.mode_change_icon()
        elif mode == 5:
            self.mode_change_turns()
        elif mode == 6:
            self.mode_explode_square()
        else:
            print("Неверно выбран режим")
            self.mode = 0

    '''def mode_help(self) -> None:  # -1
        f = open("./help", "r")
        print(f.read())
        f.close()
        self.mode = 0'''

    def mode_menu(self) -> None:  # 0
        print("Выберите режим:")
        print("1 - играть, 2 - выбрать тип, 3 - изменить размер, 4 - изменить иконку,")
        print("5 - включить/выключить ходы, 6 - взорвать клетку")
        try:
            mode = int(input("--> "))
            self.mode = mode
        except ValueError:
            print()

    def mode_play(self) -> None:  # 1
        board = self.board
        board.draw()
        king = board.check_king()
        if king != -1:
            if king == 0:
                print("Победа белых")
            elif king == 1:
                print("Победа черных")
            elif king == 2:
                print("Ничья")
            self.mode = 0
            return
        if board.get_turns_enabled():
            turn = board.get_turn()
            if turn == 0:
                print("Ход черных")
            elif turn == 1:
                print("Ход белых")

        try:
            user_input = input("Введите координаты x, y, target_x, target_y: ").split(',')
            if user_input[0] == "-":
                self.mode = 0
                return
            size = board.get_size()
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
            print("Неверный формат ввода")

    def mode_change_type(self) -> None:  # 2
        print("0 - пустое, 1 - обычное, 2 - бомбы")
        try:
            user_input = input("Введите тип поля: ")
            if user_input[0] == "-":
                pass
            self.board_type = int(user_input)
            self.setup()
        except ValueError:
            print("Неверный тип поля")
        finally:
            self.mode = 0
            print()

    def mode_change_size(self) -> None:  # 3
        try:
            user_input = input("Введите размер поля: ")
            if user_input[0] == "-":
                pass
            else:
                size = int(user_input)
                if size < 0:
                    size = 0
                self.board = Board(new_size=size, turns_enabled=self.turns_enabled)
                self.setup()
        except ValueError:
            pass
        finally:
            self.mode = 0
            print()

    def mode_change_icon(self) -> None:  # 4
        try:
            user_input = input("Введите цвет, тип фигуры и иконку: ").split(',')
            if user_input[0] == "-":
                pass
            else:
                piece_color = int(user_input[0])
                piece_type = int(user_input[1])
                new_icon = user_input[2]
                self.board.change_icon(piece_color, piece_type, new_icon)
        except (IndexError, ValueError):
            print("Неправильный формат ввода")
        finally:
            self.mode = 0
            print()

    def mode_change_turns(self) -> None:  # 5
        try:
            user_input = input("0 - выключить ходы, 1 - включить ходы: ")
            if user_input[0] == "-":
                pass
            else:
                if user_input == "0":
                    self.board.set_turns_enabled(False)
                elif user_input == "1":
                    self.board.set_turns_enabled(True)
                else:
                    print("Неправильный формат ввода")
        except ValueError:
            print("Неправильный формат ввода")
        finally:
            self.mode = 0
            print()

    def mode_explode_square(self) -> None:  # 6
        try:
            from pieces import Bomb
            self.board.draw()
            user_input = input("Введите координаты x, y взрываемой клетки: ").split(',')
            if user_input[0] == "-":
                self.mode = 0
                return
            size = self.board.get_size()
            x = convert_user_x(user_input[1], size)
            y = convert_user_y(user_input[0])
            self.board.add(Bomb(-1), x, y)
            self.board.explode(x, y)
        except (IndexError, ValueError):
            print("Неверный формат ввода")
        finally:
            self.mode = 1
