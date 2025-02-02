import weakref
from movement import *


class Piece:
    all_instances = weakref.WeakSet()
    type: str
    piece_registry = {}
    default_texture = 'NA'
    texture_registry = {
        'empty': {'w': "##", 'b': "  "},
        'pawn': {'w': "Wp", 'b': "Bp"},
        'rook': {'w': "Wr", 'b': "Br"},
        'knight': {'w': "Wk", 'b': "Bk"},
        'bishop': {'w': "Wb", 'b': "Bb"},
        'queen': {'w': "Wq", 'b': "Bq"},
        'king': {'w': "WK", 'b': "BK"},
        'bomb': {'w': "Wmb", 'b': "Bmb"}
    }
    movement_registry = {
        'empty': MovementType,
        'pawn': PawnMovement,
        'rook': RookMovement,
        'knight': KnightMovement,
        'bishop': BishopMovement,
        'queen': QueenMovement,
        'king': KingMovement,
        'bomb': KingMovement
    }
    defaults = {
        'color': 'n',
        'range': 0,
        'explosion_range': 0,
        'can_jump':  False,
        'can_eat_own':  False,
        'can_explode':  False
        }

    def __init__(self, color: str) -> None:
        self.overrides = {"color": color}
        self.__class__.instances.add(self)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.instances = (weakref.WeakSet())
        parent_defaults = getattr(super(cls, cls), "defaults", {})
        cls.defaults = {**parent_defaults, **getattr(cls, "defaults", {})}
        if hasattr(cls, 'type'):
            Piece.piece_registry[cls.type] = cls
        else:
            raise TypeError(f"У класса {cls.__name__} нет атрибута 'тип'")

    def __setattr__(self, item: str, value):
        if item == "movement_type":
            value = Piece.movement_registry.get(value, None)
            if value:
                self.overrides["movement_type"] = value
            else:
                print("Нет заданного типа движения")
                return

        elif item in self.defaults:
            value = self.convert_to_type(item, value)
            self.overrides[item] = value

        else:
            super().__setattr__(item, value)

    def __getattr__(self, item):
        if item in self.defaults:
            return self.overrides.get(item, self.defaults[item])
        raise AttributeError(f"Атрибут {item} не существует")

    @classmethod
    def set_default(cls, name, value):
        if name in cls.ults:
            cls.defaults[name] = value
            for instance in cls.instances:
                if name not in instance.overrides:
                    setattr(instance, name, value)
        else:
            raise AttributeError(f"Нет атрибута {name}")

    @property
    def color(self) -> str:
        return self.overrides.get("color", self.defaults["color"])

    @color.setter
    def color(self, value: str) -> None:
        value = value.lower().strip()
        if value in ["b", "black", "0"]:
            value = "b"
        elif value in ["w", "white", "1"]:
            value = "w"
        elif value in ["n", "none"]:
            value = "n"

        if value in ["b", "w", "n"]:
            self.overrides["color"] = value
        else:
            print(f"Не существует цвет {value}")

    @property
    def texture(self) -> str:
        if self.color in ['b', 'w']:
            return self.overrides.get("texture", self.texture_registry[self.type][self.color])
        elif self.color == 'n':
            return self.overrides.get("texture", self.default_texture)

    @texture.setter
    def texture(self, value: str) -> None:
        self.overrides["texture"] = value

    @property
    def range(self):
        return self.overrides.get('range', self.defaults['range'])

    @range.setter
    def range(self, value):
        self.overrides['range'] = max(value, -1)

    @property
    def explosion_range(self):
        return self.overrides.get('explosion_range', self.defaults['explosion_range'])

    @explosion_range.setter
    def explosion_range(self, value):
        self.overrides['explosion_range'] = max(value, 0)

    @property
    def movement_type(self) -> MovementType:
        return self.overrides.get("movement_type", self.movement_registry[self.type])

    @movement_type.setter
    def movement_type(self, value: str):
        value = Piece.movement_registry.get(value)
        if value:
            self.overrides["movement_type"] = value

    @classmethod
    def get_texture_length(cls) -> int:
        default_textures = [texture for piece_type in cls.texture_registry.values() for texture in piece_type.values()]
        custom_textures = [instance.overrides.get("texture") for instance in cls.all_instances if "texture" in instance.overrides]
        all_textures = default_textures + custom_textures + [cls.default_texture]
        all_textures = [t for t in all_textures if t is not None]
        return max(len(texture) for texture in all_textures) if all_textures else 0

    @classmethod
    def set_class_property(cls, prop_name: str, value, piece_type: str) -> None:
        if prop_name not in Piece.defaults and prop_name not in ("texture", "movement_type"):
            print(f"Атрибут {prop_name} не существует")
            return

        try:
            if prop_name in Piece.defaults and isinstance(value, str):
                value = cls.convert_to_type(prop_name, value)

            target_cls = cls.piece_registry.get(piece_type)
            if not target_cls:
                print(f"Класс {piece_type} не существует")
                return

            if prop_name == "texture":
                for color in target_cls.texture_registry[target_cls.type]:
                    target_cls.texture_registry[target_cls.type][color] = value
            elif prop_name == "movement_type":
                movement = cls.movement_registry.get(value)
                if not movement:
                    print(f"Тип движения {value} не существует")
                    return
                Piece.movement_registry[target_cls.type] = movement
            elif prop_name in cls.defaults and prop_name != 'color':
                target_cls.defaults[prop_name] = value

            for instance in target_cls.instances:
                if prop_name not in instance.overrides or prop_name == 'color':
                    if prop_name == "texture":
                        instance.texture = value
                    elif prop_name == "movement_type":
                        instance.movement_type = value
                    else:
                        setattr(instance, prop_name, value)

            print(f"Свойство {prop_name} изменено (класс)")
        except (TypeError, ValueError):
            print(f"Не удалось изменить свойство {prop_name}")

    def set_property(self, prop_name: str, value) -> None:
        if prop_name not in self.defaults and prop_name not in ("texture", "movement_type"):
            print(f"Атрибут {prop_name} не существует")
            return

        try:
            if prop_name in self.defaults and isinstance(value, str):
                value = self.convert_to_type(prop_name, value)

            if prop_name == "movement_type":
                self.movement_type = value
            else:
                self.__setattr__(prop_name, value)
            print(f"Свойство {prop_name} изменено (фигура)")

        except (TypeError, ValueError):
            print(f"Не удалось изменить свойство {prop_name}")

    def check_move(self, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        return self.movement_type.validate(self, board, x, y, target_x, target_y)

    @classmethod
    def convert_to_type(cls, prop_name: str, value):
        expected_type = type(cls.defaults[prop_name])

        if isinstance(value, expected_type):
            return value

        if isinstance(value, str):
            try:
                if expected_type == bool:
                    lower_val = value.lower()
                    if lower_val in ("true", "yes", "1"):
                        return True
                    elif lower_val in ("false", "no", "0"):
                        return False
                    else:
                        raise ValueError(f"Неправильное значение: '{value}'")
                else:
                    return expected_type(value)
            except Exception as e:
                raise TypeError(
                    f"Не получилось перевести '{value}' в "
                    f"{expected_type.__name__} для {prop_name}! ({e})"
                )
        else:
            raise TypeError(
                f"{prop_name} ожидает "
                f"{expected_type.__name__}, а не {type(value).__name__}!"
            )


class Empty(Piece):
    type = 'empty'


class Pawn(Piece):
    type = 'pawn'
    defaults = {
        'range': 2,
    }

    def check_move(self, board: list, x: int, y: int, target_x: int, target_y: int) -> bool:
        res = super().check_move(board, x, y, target_x, target_y)
        movement = self.overrides.get("movement_type", self.movement_registry[self.type])
        if movement == PawnMovement and res == 1:
            self.defaults['range'] = 1
        return res


class Rook(Piece):
    type = 'rook'
    defaults = {
        'range': -1,
    }


class Knight(Piece):
    type = 'knight'
    defaults = {
        'range': -1,
        'can_jump': True,
    }


class Bishop(Piece):
    type = 'bishop'
    defaults = {
        'range': -1,
    }


class Queen(Piece):
    type = 'queen'
    defaults = {
        'range': -1,
    }


class King(Piece):
    type = 'king'
    defaults = {
        'range': 1,
    }


class Bomb(Piece):
    type = 'bomb'
    defaults = {
        'range': 1,
        'explosion_range': 1,
        'can_eat_own': True,
        'can_explode': True
    }
