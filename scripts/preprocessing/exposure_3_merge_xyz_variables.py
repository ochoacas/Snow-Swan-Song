# Step 3: Convert XYZ to text files
import os
import pandas as pd

in_dir_xyz_months = 'outputs/oa_model_xyz_months'
out_dir_txt_months = 'outputs/oa_model_txt_months'
times = []

for xyz in os.listdir(in_dir_xyz_months):
    timestamp = xyz.split('_')[-2]
    times.append(timestamp)

nan_value = 0

df_lat = pd.read_csv(in_dir_xyz_months + '\\' + 'lat_rho_avg_1995-01_extracted.xyz', sep=' ')
df_lat.drop(df_lat.columns[[0, 1]], axis=1, inplace=True)
df_lon = pd.read_csv(in_dir_xyz_months + '\\' + 'lon_rho_avg_1995-01_extracted.xyz', sep=' ')
df_lon.drop(df_lon.columns[[0, 1]], axis=1, inplace=True)
df_mask = pd.read_csv(in_dir_xyz_months + '\\' + 'mask_rho_avg_1995-01_extracted.xyz', sep=' ')
df_mask.drop(df_mask.columns[[0, 1]], axis=1, inplace=True)

for time in list(dict.fromkeys(times)):
    time_matches = [xyz for xyz in os.listdir(in_dir_xyz_months) if time in xyz]
    time_matches = [xyz for xyz in time_matches if 'rho' not in xyz]
    dfs = [df_lat, df_lon, df_mask]
    for xyz in time_matches:
        df = pd.read_csv(in_dir_xyz_months + '\\' + xyz, sep=' ')
        df.drop(df.columns[[0, 1]], axis=1, inplace=True)
        dfs.append(df)
    df_year = pd.concat(dfs, join='outer', axis=1).fillna(nan_value)
    pd.DataFrame.to_csv(df_year, out_dir_txt_months + '\\' + time + '.txt', index=False, sep=',', na_rep='.')
    print('Merged variables: ' + out_dir_txt_months + '\\' + time + '.txt')