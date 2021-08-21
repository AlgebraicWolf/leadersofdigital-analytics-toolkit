# Interface for easy construction of composable filters
class Filter:
  def filt(self, xs: list) -> list:
    '''Process contents, return only instances that satisfy the filter'''
    pass

  # Composition of two filters  
  def __mul__(self, a):
    return ComposedFilter(self, a)

# Filter that does nothing 
class IdFilter(Filter):
  def filt(self, xs: list) -> list:
    return xs

# Characteristic filter -- filter that only allows objects for which a given
# predicate is satisfied
class CharacteristicFilter(Filter):
  def __init__(self, f):
    self.f = f

  def filt(self, xs: list) -> list:
    return list(filter(self.f, xs))

class ComposedFilter(Filter): 
  def __init__(self, a, b):
    self.fst = a
    self.snd = b

  def filt(self, xs: list) -> list:
    return self.snd.filt(self.fst.filt(xs))

# Filter that returns only the values that are greater than a given value
class GEFilter(CharacteristicFilter):
  def __init__(self, value):
    CharacteristicFilter.__init__(self, lambda x: x >= value if x is not None else True)

# Filter that returns only the values that are less than a given value
class LEFilter(CharacteristicFilter):
  def __init__(self, value):
    CharacteristicFilter.__init__(self, lambda x: x <= value if x is not None else True)

# Filter that allows only the values in the given range
class RangeFilter(ComposedFilter):
  def __init__(self, lo, hi):
    ComposedFilter.__init__(self, GEFilter(lo), LEFilter(hi))

# Filter that applies another filter to a given subfield
class FocusedFilter(CharacteristicFilter):
  def __init__(self, field: str, F):
    CharacteristicFilter.__init__(self, lambda x: True if F.filt([x[field]]) else False)