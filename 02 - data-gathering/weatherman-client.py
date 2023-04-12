import requests

_api_key = "144827f6a06410fe397d4df24f9e5c61"

def is_currently_raining():
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  complete_url = f"{base_url}appid={_api_key}&qportland"

  request = requests.get(complete_url).json()
  print(request)

  if request['current']['rain'] is not None:
      print('It is currently raining in Portland')
  else:
      print('It is not currently raining in Portland')

def will_rain_next_class():
  base_url = "http://api.openweathermap.org/data/2.5/forecast/daily"
  full_url = f"{base_url}?lat=45.5234&lon=-122.6762&appid={_api_key}"
  response = requests.get(full_url).json()

  weather = response['list'][5]['weather']
  if 'rain' in weather['description']:
    print('It will rain next class period')
  else:
     print('It will not rain next class')

is_currently_raining()
will_rain_next_class()