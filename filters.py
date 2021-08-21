import utils.monoidal_filters as mf
import utils.catamorphism as cata

def maybe_le(hi: int) -> mf.Filter:
  return cata.none_cata(hi, mf.IdFilter(), mf.LEFilter)

def maybe_ge(lo: int) -> mf.Filter:
  return cata.none_cata(lo, mf.IdFilter(), mf.GEFilter)

def maybe_range(lo: int, hi: int) -> mf.Filter:
  if (lo is None) or (hi is None):
    return mf.IdFilter()
  else:
    return mf.RangeFilter(lo, hi)

# Creates filter object with given settings 
def make_user_filter(params):
  subs_filter = mf.FocusedFilter('subs', maybe_range(params['subs_lo'], params['subs_hi']))
  likes_filter = mf.FocusedFilter('avg_likes', maybe_ge(params['avg_likes']))
  views_filter = mf.FocusedFilter('avg_view', maybe_ge(params['avg_view']))
  # TODO Add filter based on the date of last submission 

  return subs_filter * likes_filter * views_filter

# Function that filters given list of users
def filter_users(params, users):
  params = average_field('view', params)
  params = average_field('likes', params)
  filtered = make_user_filter(params).filt(users)

  return list(map(add_wellness, filtered))

# Function that adds wellness metric
def add_wellness(user) -> float:
  user['wellness'] = wellness(user)
  return user

# Function that calculates an obscure wellness metric for a given blogger 
def wellness(user) -> float:
  wellness_smth = user['avg_likes'] / user['subs']
  return min(1.00, wellness_smth / 0.05)


# Calculate average for a given field in the structure 
def average_field(field, structs):
  def single_avg(field):
    def single_avg_helper(struct):
      struct['avg_'+field] = sum(struct[field]) / len(struct[field])
      return struct

    return single_avg_helper

  return list(map(single_avg(field), structs)) 
