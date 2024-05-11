"""Library for quantities with units."""

from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from numbers import Real
from typing import Any, Final, Optional, Self, TypeAlias, overload

__all__ = [
    "BaseUnit",
    "data",
    "DerivedUnit",
    "si",
    "Unit",
    "UnitCombination",
    "UnitQuantity",
    "us",
]


MypyReal: TypeAlias = (
    Real | float | int
)  # mypy is a stupid piece of shit so this is necessary to circumvent its misconception that float and int aren't real numbers


class UnitError(ValueError):
    """Incompatible argument units."""


class UnitQuantity:
    """A quantity with units."""

    __slots__ = ("_units", "_value")

    _units: dict[Unit, float]
    _value: float

    @overload
    def __new__(cls, value: MypyReal, /) -> Self:
        """Return a dimensionless UnitQuantity."""

    @overload
    def __new__(cls, source: UnitQuantity, /) -> Self:
        """Return a UnitQuantity equivalent to source."""

    def __new__(cls, value_or_source: MypyReal | UnitQuantity, /) -> Self:
        if type(value_or_source) is cls:
            return value_or_source
        self: Final[Self] = super().__new__(cls)
        if isinstance(value_or_source, UnitQuantity):
            self._units = value_or_source._units
            self._value = value_or_source._value
        else:
            self._units = {}
            self._value = float(value_or_source)
        return self

    def __abs__(self) -> UnitQuantity:
        result: Final[UnitQuantity] = UnitQuantity(abs(self._value))
        result._units = self._units
        return result

    def __add__(self, other: UnitQuantity, /) -> UnitQuantity:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            n: Final[UnitQuantity] = self.normalize()
            result: Final[UnitQuantity] = UnitQuantity(
                n._value + other.normalize()._value
            )
            result._units = n._units
            return result.convert(self.units)
        else:
            raise UnitError("cannot add UnitQuantities with incompatible units.")

    def __bool__(self) -> bool:
        return self._value != 0.0

    def compatible(self, other: UnitQuantity, /) -> bool:
        """Return whether this UnitQuantity represents the same type of quantity as other."""
        return self.normalize()._units == other.normalize()._units

    def convert(self, units: UnitCombination, /) -> UnitQuantity:
        """Convert this UnitQuantity into one with the given units (if possible)."""
        if self.compatible(units):
            result: Final[UnitQuantity] = UnitQuantity(
                self.normalize()._value / units.normalize()._value
            )
            result._units = units._units
            return result
        else:
            raise UnitError("mismatched units for conversion.")

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self) -> Self:
        return self

    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, UnitQuantity):
            return (
                self.compatible(other)
                and self.normalize()._value == other.normalize()._value
            )
        else:
            return NotImplemented

    def __float__(self) -> float:
        """Convert this UnitQuantity to a float. The conversion will fail if this UnitQuantity has nontrivial units (units which do not cancel)."""
        if self.compatible(UnitCombination()):
            return self.normalize()._value
        else:
            raise UnitError(
                "Cannot convert UnitQuantity with nontrivial units to float."
            )

    def __ge__(self, other: UnitQuantity, /) -> bool:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            return self.normalize()._value >= other.normalize()._value
        else:
            raise UnitError("cannot compare UnitQuantites with incompatible units.")

    def __gt__(self, other: UnitQuantity, /) -> bool:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            return self.normalize()._value > other.normalize()._value
        else:
            raise UnitError("cannot compare UnitQuantites with incompatible units.")

    def __hash__(self) -> int:
        n: Final[UnitQuantity] = self.normalize()
        return hash((n._value,) + tuple(n._units.items()))

    def __le__(self, other: UnitQuantity, /) -> bool:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            return self.normalize()._value <= other.normalize()._value
        else:
            raise UnitError("cannot compare UnitQuantites with incompatible units.")

    def __lt__(self, other: UnitQuantity, /) -> bool:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            return self.normalize()._value < other.normalize()._value
        else:
            raise UnitError("cannot compare UnitQuantites with incompatible units.")

    def __mul__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        result: UnitQuantity
        if isinstance(other, UnitQuantity):
            result = UnitQuantity(self._value * other._value)
            result._units = {
                unit: self._units.get(unit, 0.0) + other._units.get(unit, 0.0)
                for unit in self._units | other._units
                if self._units.get(unit, 0.0) != -other._units.get(unit, 0.0)
            }
            return result
        elif isinstance(other, Real):
            result = UnitQuantity(self._value * other)
            result._units = self._units
            return result
        else:
            return NotImplemented

    def __neg__(self) -> UnitQuantity:
        result: Final[UnitQuantity] = UnitQuantity(-self._value)
        result._units = self._units
        return result

    def normalize(self) -> UnitQuantity:
        """Convert this UnitQuantity into one of the same value with only BaseUnits."""
        result: UnitQuantity = UnitQuantity(self._value)
        for unit, exponent in self._units.items():
            result *= unit.normalize() ** exponent
        return result

    def __pos__(self) -> Self:
        return self

    def __pow__(self, exponent: MypyReal, /) -> UnitQuantity:
        if isinstance(exponent, Real):
            result: Final[UnitQuantity] = UnitQuantity(self._value**exponent)
            result._units = (self.units**exponent)._units
            return result
        else:
            return NotImplemented

    def __repr__(self) -> str:
        if self._units:
            return f"{self._value!r} * {self.units._repr_untyped()}"
        else:
            return f"{type(self).__name__}({self._value!r})"

    def __rmul__(self, other: MypyReal, /) -> UnitQuantity:
        if isinstance(other, Real):
            result: UnitQuantity = UnitQuantity(other * self._value)
            result._units = self._units
            return result
        else:
            return NotImplemented

    def round(
        self, interval: UnitQuantity, rounding_mode: Callable[[float], int] = round
    ) -> UnitQuantity:
        """Round this value to a multiple of interval. The rounding_mode is used to determine whether to round up or down."""
        return interval * rounding_mode(float(self / interval))

    def __rtruediv__(self, other: MypyReal, /) -> UnitQuantity:
        if isinstance(other, Real):
            result: UnitQuantity = UnitQuantity(other / self._value)
            result._units = {unit: -exponent for unit, exponent in self._units.items()}
            return result
        else:
            return NotImplemented

    def __str__(self) -> str:
        return (
            f"{self._value} {self.units._str_no1()}"
            if self._units
            else str(self._value)
        )

    def __sub__(self, other: UnitQuantity, /) -> UnitQuantity:
        if not isinstance(other, UnitQuantity):
            return NotImplemented
        elif self.compatible(other):
            n: Final[UnitQuantity] = self.normalize()
            result: Final[UnitQuantity] = UnitQuantity(
                n._value - other.normalize()._value
            )
            result._units = n._units
            return result.convert(self.units)
        else:
            raise UnitError("cannot subtract UnitQuantities with incompatible units.")

    def __truediv__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        result: UnitQuantity
        if isinstance(other, UnitQuantity):
            result = UnitQuantity(self._value / other._value)
            result._units = {
                unit: self._units.get(unit, 0.0) - other._units.get(unit, 0.0)
                for unit in self._units | other._units
                if self._units.get(unit, 0.0) != other._units.get(unit, 0.0)
            }
            return result
        elif isinstance(other, Real):
            result = UnitQuantity(self._value / other)
            result._units = self._units
            return result
        else:
            return NotImplemented

    @property
    def units(self) -> UnitCombination:
        result: Final[UnitCombination] = UnitCombination()
        result._units = self._units
        return result


class UnitCombination(UnitQuantity):
    """A combination of units.
    Most of this class's behavior matches the behavior of UnitQuantity, except that *, /, and ** will return a UnitCombination if both sides are UnitCombinations.
    """

    __slots__ = ()

    @overload
    def __new__(cls) -> Self:
        """Return an empty UnitCombination."""

    @overload
    def __new__(cls, source: UnitCombination, /) -> Self:
        """Return a UnitCombination equivalent to source."""

    def __new__(cls, source: Optional[UnitCombination] = None) -> Self:
        result: Final[Self] = super().__new__(cls, 1.0)
        if source is not None:
            result._units = source._units
        return result

    @overload
    def __mul__(self, other: UnitCombination, /) -> UnitCombination:
        pass

    @overload
    def __mul__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        pass

    def __mul__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        if isinstance(other, UnitCombination):
            result: Final[UnitCombination] = UnitCombination()
            result._units = {
                unit: self._units.get(unit, 0.0) + other._units.get(unit, 0.0)
                for unit in self._units | other._units
                if self._units.get(unit, 0.0) != -other._units.get(unit, 0.0)
            }
            return result
        else:
            return super().__mul__(other)

    def __pow__(self, exponent: MypyReal, /) -> UnitCombination:
        if isinstance(exponent, Real):
            result: Final[UnitCombination] = UnitCombination()
            if exponent:
                result._units = {
                    unit: float(e * exponent) for unit, e in self._units.items()
                }
            return result
        else:
            return NotImplemented

    @overload
    def __truediv__(self, other: UnitCombination, /) -> UnitCombination:
        pass

    @overload
    def __truediv__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        pass

    def __truediv__(self, other: UnitQuantity | MypyReal, /) -> UnitQuantity:
        if isinstance(other, UnitCombination):
            result: Final[UnitCombination] = UnitCombination()
            result._units = {
                unit: self._units.get(unit, 0.0) - other._units.get(unit, 0.0)
                for unit in self._units | other._units
                if self._units.get(unit, 0.0) != other._units.get(unit, 0.0)
            }
            return result
        else:
            return super().__truediv__(other)

    def __repr__(self) -> str:
        if not self._units:
            return f"{type(self).__name__}()"
        elif len(self._units) == 1 == next(iter(self._units.values())):
            return f"{type(self).__name__}({next(iter(self._units))!r})"
        else:
            return self._repr_untyped()

    def _repr_untyped(self) -> str:
        return " * ".join(
            (
                repr(unit) + ("" if exponent == 1.0 else f"**{exponent!r}")
                for unit, exponent in self._units.items()
            )
        )

    def __str__(self) -> str:
        s: Final[str] = self._str_no1()
        return (f"1 {s}" if s.startswith("/") else s) if s else "1"

    def _str_no1(self) -> str:
        numerator: Final[list[str]] = []
        denominator: Final[list[str]] = []
        for unit, exponent in self._units.items():
            if exponent > 0:
                numerator.append(str(unit) if exponent == 1 else f"{unit}^{exponent}")
            else:
                denominator.append(
                    str(unit) if exponent == -1 else f"{unit}^{-exponent}"
                )
        if denominator:
            numerator.append("/")
        return " ".join(numerator + denominator)


class Unit(ABC, UnitCombination):
    """A unit that can be used to measure a quantity.
    Most of this class's behavior is inherited from UnitCombination, except with the addition of a string used to represent it.
    """

    __slots__ = ("_symbol",)

    _symbol: str

    def __new__(cls, symbol: str, /) -> Self:
        """Create a new unit."""
        self: Final[Self] = super().__new__(cls)
        self._symbol = symbol
        self._units = {self: 1.0}
        self._value = 1.0
        return self

    def __str__(self) -> str:
        return self.symbol

    @property
    def symbol(self) -> str:
        return self._symbol


class BaseUnit(Unit):
    """A unit that defines a type of quantity.
    Most of this class's behavior is inherited from Unit, except that its members are compared by identity.
    """

    __slots__ = ()

    def __copy__(self) -> Self:
        return type(self)(self.symbol)

    def __deepcopy__(self) -> Self:
        return self.__copy__()

    def __eq__(self, other: Any, /) -> bool:
        return object.__eq__(self, other)

    def __float__(self) -> float:
        raise UnitError("Cannot convert UnitQuantity with nontrivial units to float.")

    def __hash__(self) -> int:
        return object.__hash__(self)

    def normalize(self) -> Self:
        return self

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} {self} at 0x{hex(id(self))[2:].upper().zfill(16)}>"
        )


class DerivedUnit(Unit):
    """A unit that is defined in terms of other units."""

    __slots__ = ("_def",)

    _def: UnitQuantity

    def __new__(cls, symbol: str, value: UnitQuantity, /) -> Self:
        if value._value < 0.0:
            raise ValueError("Cannot create DerivedUnit with negative magnitude.")
        self: Final[Self] = UnitCombination.__new__(cls)
        self._def = value.normalize()
        self._symbol = symbol
        self._units = {self: 1.0}
        self._value = 1.0
        return self

    def normalize(self) -> UnitQuantity:
        return self._def

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.symbol!r}, {self.normalize()!r})"


from . import data, si, us
