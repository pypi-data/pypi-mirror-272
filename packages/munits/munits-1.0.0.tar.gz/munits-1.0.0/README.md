munits (name not capitalized) is a units library for Python. It allows quantities to be stored with their units attached, and simplifies unit conversion somewhat.
# Initial Setup
To import the munits library, use the import statement.
```python
>>> import munits
```
In the examples presented here, the contents of munits are imported directly into the mainspace.
```python
>>> from munits import *
```
# Defining Base Units
To define a base unit, use the `BaseUnit` class. For this example, we will define pixels as our base unit.
```python
>>> pixel = BaseUnit("px")
```
This creates a new unit object. To check this, we can print the new object. String representation of `BaseUnit`s is slightly altered in this documentation as the memory locations present in the actual representation change each time the module is loaded. They are omitted here for clarity.
```python
>>> pixel
<BaseUnit px>
```
munits also defines many standard units in order to improve inter&hyphen;operability of code. These are found within the `si`, `si.prefix`, `us`, and `data` sub&hyphen;modules.
```python
>>> si.METRE
<BaseUnit m>
```
Note that two `BaseUnit`s having the same symbol does not make them compare equal.
```python
>>> spam = BaseUnit("m")
>>> spam == si.METRE
False
>>> del spam  # cleaning up this demonstration
```
# Using Units
To add units to a quantity, multiply the value with the units to be applied.
```python
>>> 5 * pixel
5.0 * <BaseUnit px>
>>> 7.4 * si.METRE
7.4 * <BaseUnit m>
```
Quantities can take multiple units, as well as units with exponents.
```python
>>> 25 * si.METRE / si.SECOND
25.0 * <BaseUnit m> / <BaseUnit s>
>>> 13 * si.METRE**2
13.0 * <BaseUnit m>**2.0
>>> (13 * si.METRE)**2
169.0 * <BaseUnit m>**2.0
```
# Derived Units
Unlike the base units described above, derived units are defined in terms of other units. They can be defined using the `DerivedUnit` class.
```python
>>> megapixel = DerivedUnit("Mpx", 1e6 * pixel)
```
As described above, munits comes with many standard units, many of which are derived from other included units.
```python
>>> si.prefix.KILOMETER
DerivedUnit("km", 1000.0 * <BaseUnit m>)
>>> si.NEWTON
DerivedUnit("N", 1.0 * <BaseUnit kg> * <BaseUnit m> * <BaseUnit s>**-2.0)
```
It is also possible to create new `DerivedUnit`s using built&hyphen;in `BaseUnit`s.
```python
>>> frame = DerivedUnit("f", si.SECOND / 60)
```
# Other Classes
## `UnitQuantity`
A `UnitQuantity` represents a quantity that has units. This class supports many operations. `UnitQuantity`s can be added and subtracted with other `UnitQuantity`s that have compatible units. The `compatible` method can be used to test if two `UnitQuantity`s have compatible units. The `convert` method is used to convert between compatible units. Equality checks can be performed with any pair of `UnitQuantity`s, and comparisons (`<`, `>`, `<=`, or `>=`) can be performed with `UnitQuantity`s with compatible units. `UnitQuantity`s with units that cancel can be converted to `float`s and `float`s can be converted to `UnitQuantity`s with blank units. Other mathematical operations including multiplication and exponentiation. The `normalize` method converts a `UnitQuantity` into another of the same value with only `BaseUnit`s. The `round` method (different to build&hyphen;in `round`!) can be used to round `UnitQuantity`s, with a customizable rounding interval (for example, round to the nearest 5km) and rounding mode.
## `UnitCombination`
A subclass of `UnitQuantity` with a fixed value of 1. The main purpose is to specify a unit type without specifying a value, such as in `UnitQuantity.convert`. The `units` property of `UnitQuantity` objects also returns a value of this type.
## `Unit`
An abstract class representing a generic unit.