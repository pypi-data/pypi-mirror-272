"""Units related to amounts of information."""

from typing import Final

from . import BaseUnit, DerivedUnit

__all__ = [
    "BIT",
    "BYTE",
    "EXABIT",
    "EXABYTE",
    "EXBIBIT",
    "EXBIBYTE",
    "GIBIBIT",
    "GIBIBYTE",
    "GIGABIT",
    "GIGABYTE",
    "KIBIBIT",
    "KIBIBYTE",
    "KILOBIT",
    "KILOBYTE",
    "MEBIBIT",
    "MEBIBYTE",
    "MEGABIT",
    "MEGABYTE",
    "PEBIBIT",
    "PEBIBYTE",
    "PETABIT",
    "PETABYTE",
    "TEBIBIT",
    "TEBIBYTE",
    "TERABIT",
    "TERABYTE",
    "YOBIBIT",
    "YOBIBYTE",
    "YOTTABIT",
    "YOTTABYTE",
    "ZEBIBIT",
    "ZEBIBYTE",
    "ZETTABIT",
    "ZETTABYTE",
]

BIT: Final[BaseUnit] = BaseUnit("b")
BYTE: Final[DerivedUnit] = DerivedUnit("B", 8 * BIT)

YOTTABIT: Final[DerivedUnit] = DerivedUnit("Yb", 1e24 * BIT)
ZETTABIT: Final[DerivedUnit] = DerivedUnit("Zb", 1e21 * BIT)
EXABIT: Final[DerivedUnit] = DerivedUnit("Eb", 1e18 * BIT)
PETABIT: Final[DerivedUnit] = DerivedUnit("Pb", 1e15 * BIT)
TERABIT: Final[DerivedUnit] = DerivedUnit("Tb", 1e12 * BIT)
GIGABIT: Final[DerivedUnit] = DerivedUnit("Gb", 1e9 * BIT)
MEGABIT: Final[DerivedUnit] = DerivedUnit("Mb", 1e6 * BIT)
KILOBIT: Final[DerivedUnit] = DerivedUnit("kb", 1000 * BIT)

YOBIBIT: Final[DerivedUnit] = DerivedUnit("Yib", (1 << 80) * BIT)
ZEBIBIT: Final[DerivedUnit] = DerivedUnit("Zib", (1 << 70) * BIT)
EXBIBIT: Final[DerivedUnit] = DerivedUnit("Eib", (1 << 60) * BIT)
PEBIBIT: Final[DerivedUnit] = DerivedUnit("Pib", (1 << 50) * BIT)
TEBIBIT: Final[DerivedUnit] = DerivedUnit("Tib", (1 << 40) * BIT)
GIBIBIT: Final[DerivedUnit] = DerivedUnit("Gib", (1 << 30) * BIT)
MEBIBIT: Final[DerivedUnit] = DerivedUnit("Mib", (1 << 20) * BIT)
KIBIBIT: Final[DerivedUnit] = DerivedUnit("Kib", 1024 * BIT)

YOTTABYTE: Final[DerivedUnit] = DerivedUnit("YB", 1e24 * BYTE)
ZETTABYTE: Final[DerivedUnit] = DerivedUnit("ZB", 1e21 * BYTE)
EXABYTE: Final[DerivedUnit] = DerivedUnit("EB", 1e18 * BYTE)
PETABYTE: Final[DerivedUnit] = DerivedUnit("PB", 1e15 * BYTE)
TERABYTE: Final[DerivedUnit] = DerivedUnit("TB", 1e12 * BYTE)
GIGABYTE: Final[DerivedUnit] = DerivedUnit("GB", 1e9 * BYTE)
MEGABYTE: Final[DerivedUnit] = DerivedUnit("MB", 1e6 * BYTE)
KILOBYTE: Final[DerivedUnit] = DerivedUnit("kB", 1000 * BYTE)

YOBIBYTE: Final[DerivedUnit] = DerivedUnit("YiB", (1 << 80) * BYTE)
ZEBIBYTE: Final[DerivedUnit] = DerivedUnit("ZiB", (1 << 70) * BYTE)
EXBIBYTE: Final[DerivedUnit] = DerivedUnit("EiB", (1 << 60) * BYTE)
PEBIBYTE: Final[DerivedUnit] = DerivedUnit("PiB", (1 << 50) * BYTE)
TEBIBYTE: Final[DerivedUnit] = DerivedUnit("TiB", (1 << 40) * BYTE)
GIBIBYTE: Final[DerivedUnit] = DerivedUnit("GiB", (1 << 30) * BYTE)
MEBIBYTE: Final[DerivedUnit] = DerivedUnit("MiB", (1 << 20) * BYTE)
KIBIBYTE: Final[DerivedUnit] = DerivedUnit("KiB", 1024 * BYTE)
