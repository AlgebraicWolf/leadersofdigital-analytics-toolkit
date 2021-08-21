from .instaclient import cl
from datetime import datetime, timezone
from collections import Counter

def get_geoposition_instagram_posts_until(lat: float, lng: float, chunk_size: int, load_until_dttm: datetime):
  loc_guess = cl.location_search(lat, lng)[0]  # Taking the closes location is good enough for PoC 
  loc_guess = cl.location_complete(loc_guess)  # Fill in important fields

  last_loaded_dttm = load_until_dttm
  max_id = None

  posts = list()
  num_chunks = 0

  while last_loaded_dttm >= load_until_dttm:
    num_chunks += 1
    data = cl.location_medias_recent(location_pk=loc_guess.pk, amount=chunk_size * num_chunks)
    last_loaded_dttm = data[-1].taken_at
    posts = data
    print(data[-1].taken_at)
    print(num_chunks)
    print()

  return posts

def get_geoposition_instagram_posts(lat: float, lng: float, amount: int):
  loc_guess = cl.location_search(lat, lng)[0]  # Taking the closes location is good enough for PoC 
  loc_guess = cl.location_complete(loc_guess)  # Fill in important fields

  return cl.location_medias_recent(location_pk=loc_guess.pk, amount=amount)

def calculate_daily_stats(posts):
  dates = list(map(lambda x: x.taken_at.replace(hour=0, minute=0, second=0, microsecond=0), posts))
  c = Counter(dates)
  return c
