import json
from random import choice, randint
from argparse import ArgumentParser

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
  products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

  data = []
  for i in range(1000):

    record = {
      'user_id': choice(user_ids),
      'product': choice(products),
      'id': randint(0, 100000)
    }
    data.append(record)

  with open(args.output_file, 'w') as f:
    f.write(json.dumps(data, indent=4))
  print(f'Wrote {len(data)} records to {args.output_file}')