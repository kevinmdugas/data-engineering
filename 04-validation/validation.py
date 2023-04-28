import pandas as pd

def read_data():
  path = 'Hwy26Crashes2019_S23.csv'
  return pd.read_csv(path)


def validate_dates(crash_df):
  """This validates both the existence of a date and
  that the date itself is valid"""

  # Get total number of crash records
  total_records = crash_df.shape[0]

  # Filter out non-date columns
  dates_df = crash_df.loc[:, ['Crash Month', 'Crash Day', 'Crash Year']]

  # Validate date fields
  valid_years = dates_df[dates_df["Crash Year"] == 2019].shape[0]
  assert valid_years == total_records

  valid_months = dates_df[dates_df["Crash Month"].isin(list(range(1,13)))].shape[0]
  assert valid_months == total_records

  valid_days = dates_df[dates_df["Crash Day"].isin(list(range(1,32)))].shape[0]
  assert valid_days == total_records

  print('All rows have a valid date')


def validate_coords(crash_df):
  coord_df = crash_df.loc[:, ['Latitude Degrees', 'Longitude Degrees']]
  coord_rows = coord_df.to_dict('records')
  for row in coord_rows:
    latitude = row['Latitude Degrees']
    longitude = row['Longitude Degrees']
    assert (latitude is not None and longitude is not None) or \
      (latitude is None and longitude is None)
  
  print('All coordinates are valid')


def main():
  df = read_data()
  crash_df = df[df['Record Type'] == 1]
  validate_dates(crash_df)
  validate_coords(crash_df)

main()