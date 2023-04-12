import geojson


# Function for converting a Pandas dataframe into a GeoJSON spatial layer
def data2geojson(df, outfile, lon_field='X', lat_field='Y'):
    # First ensure there are no null values in the dataframe (bc a submodule used by the GeoJSON library can't do nulls)
    # Select numeric columns and fill NaNs with -9999
    numeric_columns = df.select_dtypes(include=['number']).columns
    for numeric_col in numeric_columns:
        df[numeric_col] = df[numeric_col].fillna(-9999)
    # df[numeric_columns] = df[numeric_columns].fillna('\"\"')
    # Select string columns and fill NaNs with ""
    string_columns = df.select_dtypes(include=['object']).columns
    for string_col in string_columns:
        df[string_col] = df[string_col].fillna('\"\"')
    # df[string_columns] = df[string_columns].fillna('\"\"')
    features = []
    df.apply(lambda x: features.append(geojson.Feature(
        geometry=geojson.Point((float(x[lon_field]),
                                float(x[lat_field]))),
        properties=(x.to_dict())
    )), axis=1)
    with open(outfile, 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)
    return features