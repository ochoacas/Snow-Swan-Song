import json
import pandas as pd
import geopy
from functools import reduce

# Create GeoJSON FeatureCollection object to store data as geographic features
geojson = {
    "type": "FeatureCollection",
    "name": "nodes",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }},
    "features": []
}

# California
df_ca = pd.read_csv('Shellfishdealers_CA.csv')
# Update place field with city, state, and country names for more accurate geocoding results
df_ca['City'] = df_ca['City'].astype(str) + ', California, United States'
df_ca['place'] = df_ca['City']

# Oregon
df_or = pd.read_csv('Shellfishdealers_OR.csv')
# Update place field with city, state, and country names for more accurate geocoding results
df_or['LocationCity'] = df_or['LocationCity'].str[0:-9]
df_or['LocationCity'] = df_or['LocationCity'].astype(str) + ', Oregon, United States'
df_or['place'] = df_or['LocationCity']

# ICSSL
df_icssl = pd.read_csv('icssl_2020-03-17.csv')
df_icssl.loc[df_icssl.State == 'CA', 'State'] = 'California'
df_icssl.loc[df_icssl.State == 'OR', 'State'] = 'Oregon'
df_icssl.loc[df_icssl.State == 'WA', 'State'] = 'Washington'
df_icssl['Location'] = df_icssl['City'].astype(str) + ', ' + df_icssl['State'].astype(str) + ', United States'
df_icssl['place'] = df_icssl['Location']

data_frames = [df_ca['place'], df_or['place'], df_icssl['place']]

df_merged = reduce(lambda left, right: pd.merge(left, right, on=['place'], how='outer'), data_frames)

pd.DataFrame.to_csv(df_merged, 'merged.txt', sep=',', na_rep='.', index=False)

# # Create a list of all places to geocode
# places = list(dict.fromkeys(df_ca['City'])) + list(dict.fromkeys(df_or['LocationCity'])) + \
#          list(dict.fromkeys(df_icssl['Location']))
# places = list(set(places))
# places.remove('SHELTOIN, Washington, United States')
# places.remove('OLMPIA, Washington, United States')
# places = sorted(places)
#
# # Initialize geocoder
# locator = geopy.Nominatim(user_agent='myGeocoder', timeout=3)
# for i, place in enumerate(places):
#     if place == 'LOPEZ, Washington, United States':
#         place = 'LOPEZ ISLAND, Washington, United States'
#     elif place == 'PEIRCE, Washington, United States':
#         place = 'PIERCE COUNTY, Washington, United States'
#     elif place == 'NORLAND, Washington, United States':
#         place = 'NORDLAND, Washington, United States'
#     # Geocode coordinates for places
#     location = locator.geocode(place)
#     # Handle exceptions for place names that could not be detected by geocoder
#     if not location:
#         if place == 'CITY OF INDUSTRY, California, United States':
#             place = 'INDUSTRY, California, United States'
#         elif place == 'SOUTH SAN F RANCISCO, California, United States':
#             place = 'SOUTH SAN FRANCISCO, California, United States'
#         elif place == 'EASTOUND, Washington, United States':
#             place = 'EASTSOUND, Washington, United States'
#         elif place == 'WILIMINGTON, California, United States':
#             place = 'WILMINGTON, California, United States'
#         elif place == 'IRWINDLE, California, United States':
#             place = 'IRWINDALE, California, United States'
#         elif place == 'NACHOTTA, Washington, United States':
#             place = 'NAHCOTTA, Washington, United States'
#         elif place == 'CITY OF COMMERCE, California, United States':
#             place = 'COMMERCE, California, United States'
#         elif place == 'LILILWAUP, Washington, United States':
#             place = 'LILLIWAUP, Washington, United States'
#         location = locator.geocode(place)
#     if not location:
#         print('Geocode failed: ' + place)
#
#     # Create GeoJSON feature and append to GeoJSON FeatureCollection
#     feature = {
#         "type": "Feature",
#         "id": int(i),
#         "properties": {
#             "name": place.upper()
#         },
#         "geometry": {
#             "type": "Point",
#             "coordinates": [location.longitude, location.latitude]
#         }
#     }
#     geojson['features'].append(feature)
#
# # Save GeoJSON file
# with open('harvest_site_locations.geojson', 'w') as f:
#     json.dump(geojson, f)
# print('GeoJSON created: harvest_site_locations.geojson')
