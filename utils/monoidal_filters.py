# Interface for easy construction of composable filters
class Filter:
  def filt(self, xs: list) -> list:
    '''Process contents, return only instances that satisfy the filter'''
    pass

  # Composition of two filters  
  def __mul__(self, a):
    class ComposedFilter(Filter): 
      def __init__(self, a, b):
        self.fst = a
        self.snd = b

      def filt(self, xs: list) -> list:
        return self.snd.filt(self.fst.filt(xs))

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
