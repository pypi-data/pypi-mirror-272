"""Units contained within the International System of Units and other units accepted for use within it."""

from typing import Final

from .. import BaseUnit, DerivedUnit

__all__ = [
    "AMPERE",
    "BECQUEREL",
    "CANDELA",
    "COULOMB",
    "FARAD",
    "GRAY",
    "HENRY",
    "HERTZ",
    "JOULE",
    "KATAL",
    "KELVIN",
    "KILOGRAM",
    "LITRE",
    "LUMEN",
    "LUX",
    "METRE",
    "MOLE",
    "NEWTON",
    "OHM",
    "PASCAL",
    "prefix",
    "RADIAN",
    "SECOND",
    "SIEMENS",
    "SIEVERT",
    "STERADIAN",
    "TESLA",
    "VOLT",
    "WATT",
    "WEBER",
]

# Base units
AMPERE: Final[BaseUnit] = BaseUnit("A")
CANDELA: Final[BaseUnit] = BaseUnit("cd")
KELVIN: Final[BaseUnit] = BaseUnit("K")
KILOGRAM: Final[BaseUnit] = BaseUnit("kg")
METRE: Final[BaseUnit] = BaseUnit("m")
MOLE: Final[BaseUnit] = BaseUnit("mol")
SECOND: Final[BaseUnit] = BaseUnit("s")

# Derived units
BECQUEREL: Final[DerivedUnit] = DerivedUnit("Bq", SECOND**-1)
COULOMB: Final[DerivedUnit] = DerivedUnit("C", SECOND * AMPERE)
FARAD: Final[DerivedUnit] = DerivedUnit(
    "F", KILOGRAM**-1 * METRE**-2 * SECOND**4 * AMPERE**2
)
GRAY: Final[DerivedUnit] = DerivedUnit("Gy", METRE**2 * SECOND**-2)
HENRY: Final[DerivedUnit] = DerivedUnit(
    "H", KILOGRAM * METRE**2 * SECOND**-2 * AMPERE**-2
)
HERTZ: Final[DerivedUnit] = DerivedUnit("Hz", SECOND**-1)
JOULE: Final[DerivedUnit] = DerivedUnit("J", KILOGRAM * METRE**2 * SECOND**-2)
KATAL: Final[DerivedUnit] = DerivedUnit("kat", SECOND**-1 * MOLE)
LITRE: Final[DerivedUnit] = DerivedUnit("L", 1e-3 * METRE**3)
LUX: Final[DerivedUnit] = DerivedUnit("lx", CANDELA * METRE**-1)
NEWTON: Final[DerivedUnit] = DerivedUnit("N", KILOGRAM * METRE * SECOND**-2)
OHM: Final[DerivedUnit] = DerivedUnit(
    "Ω", KILOGRAM * METRE**2 * SECOND**-3 * AMPERE**-2
)
PASCAL: Final[DerivedUnit] = DerivedUnit("Pa", KILOGRAM * METRE * SECOND**-2)
RADIAN: Final[DerivedUnit] = DerivedUnit("rad", METRE / METRE)
SIEMENS: Final[DerivedUnit] = DerivedUnit(
    "S", KILOGRAM**-1 * METRE**-2 * SECOND**3 * AMPERE**2
)
SIEVERT: Final[DerivedUnit] = DerivedUnit("Sv", METRE**2 * SECOND**-2)
STERADIAN: Final[DerivedUnit] = DerivedUnit("sr", RADIAN**2)
LUMEN: Final[DerivedUnit] = DerivedUnit("lm", CANDELA * STERADIAN)
TESLA: Final[DerivedUnit] = DerivedUnit("T", KILOGRAM * SECOND**-2 * AMPERE**-1)
VOLT: Final[DerivedUnit] = DerivedUnit(
    "V", KILOGRAM * METRE**2 * SECOND**-3 * AMPERE**-1
)
WATT: Final[DerivedUnit] = DerivedUnit("W", KILOGRAM * METRE**2 * SECOND**-3)
WEBER: Final[DerivedUnit] = DerivedUnit(
    "Wb", KILOGRAM * METRE**2 * SECOND**-2 * AMPERE**-1
)

from . import prefix
