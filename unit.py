
class UnrecognizedUnitException(Exception):
    def __init__(self, unit):
        self.message = "Unrecognized Unit encountered: " + str(unit)


class DuplicateUnitException(Exception):
    def __init__(self, message):
        self.message = message


class DuplicateDimensionException(Exception):
    def __init__(self, message):
        self.message = message


class Dimension:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    def name(self):
        return self._name

    def symbol(self):
        return self._symbol


class SimpleDimension(Dimension):
    def __init__(self, name, symbol, base_unit_name, base_unit_symbol):
        super().__init__(name, symbol)
        self._base_unit = BaseUnit(base_unit_name, base_unit_symbol, self)
        self._other_units_by_name = {}
        self._other_units_by_symbol = {}

    def base_unit(self):
        return self._base_unit

    def add_other_unit(self, unit):
        if not isinstance(unit, SimpleUnit):
            raise TypeError

        if unit.name() in self._other_units_by_name:
            raise DuplicateUnitException

        if unit.symbol() in self._other_units_by_symbol:
            raise DuplicateUnitException

        if self._base_unit == unit:
            raise DuplicateUnitException

        self._other_units_by_name[unit.name()] = unit
        self._other_units_by_symbol[unit.symbol()] = unit


class CompoundDimension(Dimension):
    pass


class Unit:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    def name(self):
        return self._name

    def symbol(self):
        return self._symbol

    def __str__(self):
        return self.symbol()


class BaseUnit(Unit):
    def __init__(self, name, symbol, dimension):
        super().__init__(name, symbol)
        self._dimension = dimension

    def dimension(self):
        return self._dimension


class SimpleUnit(Unit):
    def __init__(self, name, symbol, dimension, to_base, from_base):
        super().__init__(name, symbol)
        self._dimension = dimension
        self._to_base = to_base
        self._from_base = from_base

    def dimension(self):
        return self._dimension

    def to_base(self):
        return self._to_base

    def from_base(self):
        return self._from_base


class Quantity:

    def __init__(self, amount, unit):
        self._amount = amount
        self._unit = unit

    def amount(self):
        return self._amount

    def unit(self):
        return self._unit

    def __str__(self):
        return str(self.amount()) + " " + str(self.unit())


class MeasurementSystem:
    def __init__(self):
        self._units_by_name = {}
        self._units_by_symbol = {}
        self._simple_dimensions_by_name = {}
        self._simple_dimensions_by_symbol = {}

    def quantity(self, amount, unit):
        if not isinstance(amount, float) and not isinstance(amount, int):
            raise TypeError("Error creating a new Quantity! Amount was the wrong datatype: " + str(type(amount)))

        if not isinstance(unit, Unit):
            raise TypeError("Error creating new Quantity! Unit was the wrong datatype: " + str(type(unit)))

        if not self.contains_unit(unit):
            raise UnrecognizedUnitException("Unrecognized Unit encountered: " + str(unit))

        return Quantity(amount, unit)

    def create_unit(self, name, symbol):
        if not isinstance(name, str):
            raise TypeError("The name of a new unit was of the incorrect type! " + str(type(name)))

        if not isinstance(symbol, str):
            raise TypeError("The symbol of a new unit was of the incorrect type! " + str(type(symbol)))

        u = Unit(name, symbol)
        self._units_by_symbol[symbol] = u
        self._units_by_name[symbol] = u
        return u

    def contains_unit(self, unit):
        if not isinstance(unit, Unit):
            return False

        a = unit.name() in self._units_by_name
        b = unit.symbol() in self._units_by_symbol

        if not a and not b:
            return False

        return True

    def get_unit_by_name(self, name):
        return self._units_by_name[name]

    def get_unit_by_symbol(self, symbol):
        return self._units_by_symbol[symbol]

    def create_simple_dimension(self, name, symbol, base_unit_name, base_unit_symbol):

        if not isinstance(name, str):
            raise TypeError("New Base Dimension Name must be a String, but was: " + str(type(name)))

        if not isinstance(symbol, str):
            raise TypeError("New Base Dimension Symbol must be a String, but was: " + str(type(symbol)))

        if not isinstance(base_unit_name, str):
            raise TypeError("New Base Unit Name must be a String, but was: " + str(type(base_unit_name)))

        if not isinstance(base_unit_symbol, str):
            raise TypeError("New Base Unit Symbol must be a String, but was: " + str(type(base_unit_symbol)))

        if base_unit_name in self._units_by_name:
            raise DuplicateUnitException("Attempted to create a new Simple Dimension with an already existent Base Unit Name: " + base_unit_name)

        if base_unit_symbol in self._units_by_symbol:
            raise DuplicateUnitException("Attempted to create a new Simple Dimension with an already existent Base Unit Symbol: " + base_unit_name)

        if name in self._simple_dimensions_by_name:
            raise DuplicateUnitException("Attempted to create a new Simple Dimension with an already existent Name: " + name)

        if symbol in self._simple_dimensions_by_symbol:
            raise DuplicateUnitException("Attempted to create a new Simple Dimension with an already existent Symbol: " + symbol)

        d = SimpleDimension(name, symbol, base_unit_name, base_unit_symbol)
        self._simple_dimensions_by_name[name] = d
        self._simple_dimensions_by_symbol[symbol] = d
        self._units_by_name[base_unit_name] = d.base_unit()
        self._units_by_symbol[base_unit_symbol] = d.base_unit()
        return d

    def get_simple_dimension_by_name(self, name):
        return self._simple_dimensions_by_name[name]

    def get_simple_dimension_by_symbol(self, symbol):
        return self._simple_dimensions_by_symbol[symbol]
