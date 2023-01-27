# Step 6: Extract variables into separate time series
import pandas as pd

# Set input and output directories
in_dir_time_series = 'outputs/oa_model_time_series'
out_dir_time_series_variables = 'outputs/oa_model_time_series_variables'
variables = ['omega_arag', 'pCO2', 'pH', 'salt', 'temp']

df = pd.read_csv(in_dir_time_series + '\\oa_model_time_series.txt', sep=',')
df_lat_lon_mask = df[df.columns[0:3]]
for variable in variables:
    dfs = [df_lat_lon_mask]
    df_variable = df.filter(like=variable, axis=1)
    dfs.append(df_variable)
    df_variable_time_series = pd.concat(dfs, join='outer', axis=1)
    dfs = []
    df_variable_time_series = df_variable_time_series[df_variable_time_series['mask_1995-01'] == 1]  # filter out mask
    pd.DataFrame.to_csv(df_variable_time_series,
                        out_dir_time_series_variables + '\\oa_model_time_series_' + variable + '.txt',
                        index=False, sep=',', na_rep='.')
    df_variable_time_series = []
    print('Split time series by variable: ' + out_dir_time_series_variables +
          '\\oa_model_time_series_' + variable + '.txt')