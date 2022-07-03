from enum import Enum


class RailTypologyEnum(Enum):
    PLAQUE = "Placa"
    BALLAST = "Balasto"

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)


class RailArmamentEnum(Enum):
    WOOD = "Madera"
    MONOBLOCK = "Monoblock"
    STEDEF = "Stedef"
    DIRECT_FASTENING = "S.Directa"

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)


class RailCirculationCategory(Enum):
    CIRCULATION = "Circulacion"
    SECONDARY = "Apartado"
    GARAGE = "Talleres"

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)


class RailDirection(Enum):
    ASCENDANT = "A"
    FALLING = "D"
    ASC_N_FALL = "AD"

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)


class RailTypologyCode(Enum):
    D1 = "D1"  # switch-switch
    D2 = "D2"  # BA-switch
    D3 = "D3"  # PL-switch
    P1 = "P1"  # level_crossing-level_crossing
    P2 = "P2"  # BA-level_crossing
    BAPL = 'BA-PL'  # ballast-plaque
    PLBA = 'PL-BA'  # plaque-ballast
    PNDS = 'PN-DS'  # level_crossing-switch
    DSPN = 'DS-PN'  # switch-level_crossing
    # Basics rail typologies
    BA = "BA"  # Ballast
    PL = "PL"  # Plaque
    DS = 'DS'  # Switch
    ES = "ES"  # Station
    PN = "PN"  # Level_crossing

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)


class RailGeometryEnum(Enum):
    STRAIGHT = "Recta"
    CIRCULAR = "Circular"
    CLOTOID = "Clotoide"

    @classmethod
    def values(cls):
        return tuple(i.value for i in cls)

    @classmethod
    def items(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def description(cls):
        return tuple((i.value, i.name) for i in cls)
