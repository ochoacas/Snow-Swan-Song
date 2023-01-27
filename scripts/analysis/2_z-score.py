import pandas as pd
infile = 'PATH_TO_CSV_FILE'
df = pd.read_csv(infile)
cols = list(df.columns)
fields_to_remove = ['STATES', 'NAME']  # If columns aren't numeric, no z-score can be calculated
# fields_to_remove = ['HUC8', 'NAME']
for field in fields_to_remove:
    cols.remove(field)
for col in cols:
    col_zscore = col + '_zscore'
    df[col_zscore] = (df[col] - df[col].mean()) / df[col].std(ddof=0)
outfile = infile.replace('.csv', '_zscores.csv')
df.to_csv(outfile)
