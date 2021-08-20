def none_cata(value, default, f):
  if value is None:
    return default
  else:
    return f(value)