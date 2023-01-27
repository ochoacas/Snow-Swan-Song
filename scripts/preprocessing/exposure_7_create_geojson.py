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
                        "int": round(mean_yearly_hot_spots, 4),  # mean intensity of hot spot
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
