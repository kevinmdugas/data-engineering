import pandas as pd


def aggregate_counties():
  cols = ['State', 'County', 'TotalPop', 'Poverty', 'IncomePerCap']
  census_df = pd.read_csv('acs2017_census_tract_data.csv', usecols=cols)
  rows = census_df.to_dict('records')

  agg = {}
  id = 0
  for row in rows:
    if row['TotalPop'] > 0:
      county = f'{row["County"]}, {row["State"]}'
      if county not in agg.keys():
        id += 1
        agg[county] = {
          "ID": id,
          "Name": row['County'].split(" County")[0],
          "State": row['State'],
          "Population": row['TotalPop'],
          "Poverty": [row['Poverty']],
          "PerCapitaIncome": [row['IncomePerCap']]
        }
      else:
        agg[county]['Population'] += row['TotalPop']
        agg[county]['Poverty'].append(row['Poverty'])
        agg[county]['PerCapitaIncome'].append(row['IncomePerCap'])

  county_rows = []
  for key in agg.keys():
    county = agg[key]
    county['Poverty'] = sum(county['Poverty']) / len(county['Poverty'])
    county['PerCapitaIncome'] = sum(county['PerCapitaIncome']) / len(county['PerCapitaIncome'])
    county_rows.append(county)
  
  return pd.DataFrame.from_records(county_rows, index=['Name', 'State'])


def aggregate_covid(county_df):
  covid_df = pd.read_csv('COVID_county_data.csv')
  rows = covid_df.to_dict('records')

  agg = {}
  for row in rows:
    county = (row['county'].split(' City')[0], row['state'])
    month = row['date'].split('-')[1]
    key = f'{county}|{month}'
    if row['county'] not in ['Unknown']:
      if key not in agg.keys():
        agg[key] = {
          'ID': county_df.loc[county]['ID'],
          'Month': month,
          'Cases': row['cases'],
          'Deaths': row['deaths'],
        }
      else:
        agg[key]['Cases'] = row['cases']
        agg[key]['Deaths'] = row['deaths']

  print(agg.values())

def main():
  county_df = aggregate_counties()
  aggregate_covid(county_df)


main()