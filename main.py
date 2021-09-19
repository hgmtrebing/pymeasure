from unit import *

if __name__ == '__main__':
    m = MeasurementSystem()
    d = m.create_simple_dimension("length", "l", "meter", "m")
    q = m.quantity(45.9, d.base_unit())
    print(q)
    print(q.unit().dimension())
