import pandas as pd 
from datetime import datetime, timedelta

def read_data():
  # Read first line, remove newline char, split into column names
  path = './bc_trip259172515_230215.csv'
  with open(path) as f:
    cols = f.readline()[:-1].split(',')

  # Filter out unwanted columns
  unwanted_cols = ['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP']
  filtered_cols = list(filter(lambda col: col not in unwanted_cols, cols))
  
  # Construct dataframe
  return pd.read_csv(path, usecols=filtered_cols)

def create_timestamps(df):
  timestamps = []

  def decode_time(row):
    # Extract datetime info
    row_dict = row.to_dict()
    date = row_dict['OPD_DATE'].split(':')[0]
    seconds = row_dict['ACT_TIME']

    # Convert seconds to a time
    delta = timedelta(seconds=seconds)

    # Create timestamp and append to list of timestamps
    timestamp = datetime.strptime(f'{date}:{str(delta)}', '%d%b%Y:%H:%M:%S')
    timestamps.append(pd.Timestamp(timestamp))

  # Map function across rows to collect timestamps
  df.apply(decode_time, axis=1)

  # Insert timestamp column and drop uneeded columns
  df.insert(1, "Timestamp", timestamps, True)
  df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])

def main():
  df = read_data()
  create_timestamps(df)

main()