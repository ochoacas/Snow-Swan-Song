import pandas as pd
from datetime import date

states = ['WA', 'OR', 'CA']
dfs = []

for state in states:
    df = pd.read_html('https://www.cfsanappsexternal.fda.gov/scripts/shellfish/sh/shippers.cfm?country=US&state='
                      + state, header=0)[1]
    dfs.append(df)

pd.concat(dfs).to_csv('icssl_' + str(date.today()) + '.csv', index=False)

print('Data parsed!')
