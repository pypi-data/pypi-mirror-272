"""Units contained in the US customary system."""

from typing import Final

from . import DerivedUnit
from .si import METRE, SECOND
from .si.prefix import (
    CENTURY,
    DAY,
    DECADE,
    GRAM,
    HOUR,
    MILLENNIUM,
    MILLILITRE,
    MILLIMETRE,
    MILLISECOND,
    MINUTE,
    WEEK,
    YEAR,
)

__all__ = [
    "ACRE",
    "CENTURY",
    "CUP",
    "DAY",
    "DECADE",
    "FLUID_OUNCE",
    "FOOT",
    "GALLON",
    "HOUR",
    "INCH",
    "MILE",
    "MILLENNIUM",
    "MILLISECOND",
    "MINUTE",
    "OUNCE",
    "PINT",
    "POUND",
    "QUART",
    "SECOND",
    "TABLESPOON",
    "TEASPOON",
    "TON",
    "WEEK",
    "YARD",
    "YEAR",
]

INCH: Final[DerivedUnit] = DerivedUnit("in.", 25.4 * MILLIMETRE)
FOOT: Final[DerivedUnit] = DerivedUnit("ft.", 12 * INCH)
YARD: Final[DerivedUnit] = DerivedUnit("yd.", 3 * FOOT)
MILE: Final[DerivedUnit] = DerivedUnit("mi.", 5280 * FOOT)

ACRE: Final[DerivedUnit] = DerivedUnit(
    "acre", 4046.8564224 * METRE**2
)  # Wierd definition due to survey foot being slightly different from standard foot defined above.

TEASPOON: Final[DerivedUnit] = DerivedUnit("tsp.", 4.92892159375 * MILLILITRE)
TABLESPOON: Final[DerivedUnit] = DerivedUnit("tbsp.", 3 * TEASPOON)
FLUID_OUNCE: Final[DerivedUnit] = DerivedUnit("fl. oz.", 2 * TABLESPOON)
CUP: Final[DerivedUnit] = DerivedUnit("c.", 8 * FLUID_OUNCE)
PINT: Final[DerivedUnit] = DerivedUnit("pt.", 2 * CUP)
QUART: Final[DerivedUnit] = DerivedUnit("qt.", 2 * PINT)
GALLON: Final[DerivedUnit] = DerivedUnit("gal.", 4 * QUART)

OUNCE: Final[DerivedUnit] = DerivedUnit("oz.", 28.349523125 * GRAM)
POUND: Final[DerivedUnit] = DerivedUnit("lb.", 16 * OUNCE)
TON: Final[DerivedUnit] = DerivedUnit("t.", 2000 * POUND)
