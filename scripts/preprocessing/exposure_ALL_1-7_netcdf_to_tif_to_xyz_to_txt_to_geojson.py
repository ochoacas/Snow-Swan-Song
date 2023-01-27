# Overall script for converting NetCDF files into GeoJSON time series with hotspot threshold for omega_arag <= 1.4
# Estimated time to run to completion: 1 hr 23 min; Memory required to save intermediate files: ~60 GB
# Once GeoJSON output is created for OA hotspots, use QGIS to clip points by a 5-km buffer of study area polygon

# Step 1: Convert NetCDF to GeoTIFF
import gdal
import netCDF4
import sys

in_dir_nc = 'inputs/oa_model_nc/hauri_et_al_2013'  # Start by declaring path to directory of NetCDF files (e.g. avg_1995_extracted.nc)
out_dir_tif_years = 'outputs/oa_model_tif_years'
out_dir_tif_months = 'outputs/oa_model_tif_months'
years = range(1995, 2051)
months = [month for month in range(1, 13)]

for i, month in enumerate(months):
    if i < 9:
        months[i] = '0' + str(month)
    else:
        months[i] = str(month)

translate_options = gdal.TranslateOptions(format='GTiff', outputSRS='EPSG:3857')

for year in years:
    in_file_nc = 'avg_' + str(year) + '_extracted.nc'
    subvars = netCDF4.Dataset(sys.path[0] + '\\' + in_dir_nc + '\\' + in_file_nc, mode='r').variables.keys()
    subvars = [key for key in subvars]
    subvars.remove('time')
    for subvar in subvars:
        try:
            src_ds_nc = gdal.Open('NETCDF:{0}:{1}'.format(sys.path[0] + '\\' + in_dir_nc + '\\' + in_file_nc, subvar))
            out_ds_tif_year = out_dir_tif_years + '\\' + subvar + '_' + in_file_nc.replace('.nc', '.tif')
            gdal.Translate(out_ds_tif_year, src_ds_nc, options=translate_options)
            print('Translated: ' + in_file_nc + ' --> ' + out_ds_tif_year)
            src_ds_nc = None
            out_ds_tif_year = None
        except:
            print('Could not open: ' + in_file_nc + ':' + subvar)
            src_ds_nc = None
            out_ds_tif_year = None
            pass
    in_file_nc = None
    for subvar in subvars:
        in_file_tif_year = subvar + '_avg_' + str(year) + '_extracted.tif'
        src_ds_tif_year = gdal.Open(sys.path[0] + '\\' + out_dir_tif_years + '\\' + in_file_tif_year)
        for i, month in enumerate(months):
            translate_options_month = gdal.TranslateOptions(format='GTiff', outputSRS='EPSG:3857', bandList=[i + 1])
            out_ds_tif_month = sys.path[0] + '\\' + out_dir_tif_months + '\\' + \
                               in_file_tif_year.replace(str(year), str(year) + '-' + str(month))
            try:
                gdal.Translate(out_ds_tif_month, src_ds_tif_year, options=translate_options_month)
                print('Split band: ' + in_file_tif_year + ' --> ' + out_ds_tif_month)
                out_ds_tif_month = None
            except:
                print('Could not open: ' + in_file_tif_year)
                in_file_tif = None
                src_ds_tif_year = None
                out_ds_tif_month = None
                pass
        in_file_tif = None
        src_ds_tif_year = None
        out_ds_tif_month = None

# Step 2: Convert GeoTIFF to XYZ
import gdal
import os
import sys

in_dir_tif_months = 'outputs/oa_model_tif_months'
out_dir_asc_months = 'outputs/oa_model_asc_months'
out_dir_xyz_months = 'outputs/oa_model_xyz_months'

translate_options1 = gdal.TranslateOptions(format='AAIGrid', outputSRS='EPSG:3857')
translate_options2 = gdal.TranslateOptions(format='XYZ', outputSRS='EPSG:4326')

for in_tif in os.listdir(in_dir_tif_months):
    src_ds = sys.path[0] + '\\' + in_dir_tif_months + '\\' + in_tif
    out_ds = sys.path[0] + '\\' + out_dir_asc_months + '\\' + in_tif.replace('.tif', '.asc')
    gdal.Translate(out_ds, src_ds, options=translate_options1)
    print('Translated: ' + in_tif + ' --> ' + out_ds)
    src_ds = None
    out_ds = None

for in_asc in os.listdir(out_dir_asc_months):
    if '.xml' in in_asc:
        continue
    elif '.prj' in in_asc:
        continue
    else:
        src_ds = sys.path[0] + '\\' + out_dir_asc_months + '\\' + in_asc
        out_ds = sys.path[0] + '\\' + out_dir_xyz_months + '\\' + in_asc.replace('.asc', '.xyz')
        gdal.Translate(out_ds, src_ds, options=translate_options2)
        print('Translated: ' + in_asc + ' --> ' + out_ds)
        src_ds = None
        out_ds = None

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

# Step 7: Summarize text files and convert to GeoJSON
import pandas as pd
from datetime import datetime
import json

# Set input and output directories
in_dir_time_series_variables = 'outputs/oa_model_time_series_variables'

# variables = ['omega_arag', 'pCO2', 'pH', 'salt', 'temp']
variables = ['omega_arag']

# Create GeoJSON FeatureCollection object to store data as geographic features
geojson = {
    "type": "FeatureCollection",
    "name": "hotspots",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }},
    "features": []
}


def average(lst):
    return sum(lst) / len(lst)


for variable in variables:
    df = pd.read_csv(in_dir_time_series_variables + '\\oa_model_time_series_' + variable + '.txt', sep=',')
    df = df.T
    x = [item.split('_')[-1] for item in list(df.index)[3:]]  # times
    x = [datetime.strptime(time, '%Y-%m') for time in x]
    for i, point in enumerate(df.columns):
        lat, lon = df[i][0], df[i][1]
        y = df[i][3:].rolling(window=360).mean()  # calculate avg over 360 months (i.e 30 years)
        min_value = df[i][3:].rolling(window=360).min()
        max_value = df[i][3:].rolling(window=360).max()

        # Create a list of hot spot occurrences
        hot_spots = []
        for t, time in enumerate(x):
            time = time.strftime('%Y-%m')
            value = df[i][t + 3]
            if variable != 'omega_arag':
                continue
            if value <= 1.4:
                hot_spots.append({
                    "time": time,
                    "value": value
                })
        if len(hot_spots) != 0:
            hot_spot_values, hot_spot_months, hot_spot_years = [], [], []
            for hot_spot in hot_spots:
                hot_spot_value = hot_spot["value"]
                hot_spot_values.append(hot_spot_value)
                hot_spot_month = hot_spot["time"].split('-')[1]
                hot_spot_months.append(int(hot_spot_month))
                hot_spot_year = hot_spot["time"].split('-')[0]
                hot_spot_years.append(int(hot_spot_year))

            hot_spot_mean = average(hot_spot_values)
            hot_spot_month_mean = average(hot_spot_months)
            for year in hot_spot_years:
                yearly_hot_spots = []
                for hot_spot in hot_spots:
                    if int(hot_spot["time"].split('-')[0]) != year:
                        continue
                    yearly_hot_spots.append(hot_spot["value"])
                mean_yearly_hot_spots = average(yearly_hot_spots)
                ct_yearly_hot_spots = len(yearly_hot_spots)
                # Create GeoJSON feature and append to GeoJSON FeatureCollection
                feature_hotspot = {
                    "type": "Feature",
                    "id": (int(i) + 1) * 10000 + year,
                    "properties": {
                        "year": str(year),
                        "freq": ct_yearly_hot_spots,  # months/yr below threshold
                        "int": round(mean_yearly_hot_spots, 4)  # mean intensity of hot spot
                        # "year": str(year) + '-01',
                        # "start_30yrAvg": round(y[y.first_valid_index()], 4),
                        # "end_30yrAvg": round(y[-1], 4),
                        # "start_30yrMin": round(min_value[min_value.first_valid_index()], 4),
                        # "end_30yrMin": round(min_value[-1], 4),
                        # "start_30yrMax": round(max_value[max_value.first_valid_index()], 4),
                        # "end_30yrMax": round(max_value[-1], 4)
                        # "time_1st_hot_spot": hot_spots[0][0],
                        # "time_hot_spot": hot_spots[h][0],
                        # "mean_month_hot_spot": round(hot_spot_month_mean, 4),
                        # "value_hot_spot": round(hot_spot_value, 4),
                        # "month_hot_spot": int(hot_spot_month),
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    }
                }
                geojson['features'].append(feature_hotspot)

        print("Iterated through point " + str(i) + " of " + str(len(df.columns)))

    # Save GeoJSON file
    with open('outputs/' + variable + '_hotspots_' + datetime.now().strftime('%Y-%m-%d_%H%M')
              + '.geojson', 'w') as f:
        json.dump(geojson, f)

    # Reset GeoJSON FeatureCollection object
    geojson = {
        "type": "FeatureCollection",
        "name": "hotspots",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }},
        "features": []
    }

print("Completed conversion of NetCDF to GeoJSON!")
