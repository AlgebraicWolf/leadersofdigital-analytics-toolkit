from instaclient import cl

def get_geoposition_instagram_stats(lat: float, lng: float, date_at_least: datetime.datetime):
  loc_guess = cl.location_search(lat, lng)[0]  # Taking the closes location is good enough for PoC 
  loc_guess = cl.location_complete(loc_guess)  # Fill in important fields

  posts = cl.location_medias_recent(loc_guess.pk, amount)
  post_dates = list(map(lambda x: x.taken_at, posts))
  return post_dates
  