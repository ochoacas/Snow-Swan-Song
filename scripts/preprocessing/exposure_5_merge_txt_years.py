# Step 5: Merge text files into overall time series
import pandas as pd

# Set input and output directories
in_dir_txt_years = 'outputs/oa_model_txt_years'
out_dir_time_series = 'outputs/oa_model_time_series'
years = range(1995, 2051)
variables = ['lat', 'lon', 'mask', 'omega_arag', 'pCO2', 'pH', 'salt', 'temp']
nan_value = 0
timestamps = []
dfs = []
for year in years:
    df = pd.read_csv(in_dir_txt_years + '\\' + str(year) + '.txt', sep=',')
    if year != 1995:
        df.drop(df.columns[[0, 1, 2]], axis=1, inplace=True)  # only need lat, lon, and mask columns once in output
    dfs.append(df)
df_all_years = pd.concat(dfs, join='outer', axis=1).fillna(nan_value)
dfs = []
pd.DataFrame.to_csv(df_all_years, out_dir_time_series + '\\oa_model_time_series.txt', index=False, sep=',', na_rep='.')
print('Merged years: ' + out_dir_time_series + '\\oa_model_time_series.txt')