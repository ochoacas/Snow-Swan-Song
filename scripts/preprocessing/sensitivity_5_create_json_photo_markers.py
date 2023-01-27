import pandas as pd
import json

# Set input and output directories
infile = 'inputs/CSV_FILE_NAME'  # input CSV file with list of image URL's and coordinates
outfile = 'outputs/photos.json'

photos = []

df = pd.read_csv(infile, sep=',', encoding='ISO-8859-1')

for i, j in df.iterrows():
    photo = {
        'url': j['url'],
        'thumbnail': j['url'],
        'source': j['source'],
        'caption': j['NAMELSAD'],
        'lat': j['INTPTLAT'],
        'lng': j['INTPTLON'],
        'geoid': j['GEOID'],
    }
    photos.append(photo)

# Save JSON file
with open(outfile, 'w') as f:
    json.dump(photos, f)
