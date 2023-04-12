# Import libraries
import os  # used to create path variables for input and output file locations
import pandas as pd  # used to read CSV data
import helper_functions as hf  # used to convert CSV data to GeoJSON

# Define path to input file
infile = os.path.join('inputs', 'snowpack_fig-1.csv')

# Define path of output file
outfile = os.path.join('outputs', 'snowpack_changes_1955-2022.geojson')

# Read input file as a dataframe
df = pd.read_csv(infile, skiprows=6)  # first six rows skipped

# Save the input dataframe as a GeoJSON output file
hf.data2geojson(df, outfile, lon_field='Longitude', lat_field='Latitude')

# Print a success message
print('Completed: {}'.format(outfile))
