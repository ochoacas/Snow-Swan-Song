# Step 4: Summarize text files by year
import pandas as pd

# Set input and output directories
in_dir_txt_months = 'outputs/oa_model_txt_months'
out_dir_txt_years = 'outputs/oa_model_txt_years'
years = range(1995, 2051)
months = [month for month in range(1, 13)]
for i, month in enumerate(months):
    if i < 9:
        months[i] = '0' + str(month)
    else:
        months[i] = str(month)
variables = ['lat', 'lon', 'mask', 'omega_arag', 'pCO2', 'pH', 'salt', 'temp']
nan_value = 0
timestamps = []
for year in years:
    dfs = []
    for month in months:
        timestamp = str(year) + '-' + str(month)
        if timestamp not in timestamps:
            timestamps.append(timestamp)
        df = pd.read_csv(in_dir_txt_months + '\\' + timestamp + '.txt', sep=',',
                         names=[variable + '_' + str(year) + '-' + str(month) for variable in variables])
        if month != '01':
            df.drop(df.columns[[0, 1, 2]], axis=1, inplace=True)  # only need lat, lon, and mask columns once in output
        dfs.append(df)

    df_year = pd.concat(dfs, join='outer', axis=1).fillna(nan_value)
    timestamps = []
    pd.DataFrame.to_csv(df_year, out_dir_txt_years + '\\' + str(year) + '.txt', index=False, sep=',', na_rep='.')
    print('Merged months: ' + out_dir_txt_years + '\\' + str(year) + '.txt')