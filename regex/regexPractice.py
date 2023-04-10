import re

def regex_checker(i):
  exc = {
    '^\w+$': ['abcd', 'a', '*2', 'a+']
  }

  p = list(exc.keys())[i]
  print(f'\npattern: {p}')

  def match(p, str):
    match = not bool(re.match(p,str) is None)
    print (f'{str}: {match}')

  list(map(lambda str: match(p, str), exc[p]))

regex_checker(0)
