from utils import monoidal_filters as mf

odds = mf.CharacteristicFilter(lambda x: x % 2 == 1)
multiples_of_three = mf.CharacteristicFilter(lambda x : x % 3 == 0)
identity = mf.IdFilter()

composite = odds * multiples_of_three * identity

print(composite.filt(list(range(1, 100))))