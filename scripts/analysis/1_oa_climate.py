# Optional Step: Calculate 30-year baseline OA climate at start/end of time series, and change in 30-year mean
# Outputs GeoTIFF files
# Calculate change in 30-year averages of climate model variables
import sys
import gdal_calc

# Set input & output directories. Input directory should contain annual GeoTIFF files with 12 bands representing months.
in_dir = sys.path[0] + '/../preprocessing/outputs/oa_model_tif_years'
out_dir = sys.path[0] + '/outputs/'

# Set time range and sub-ranges. Sub-ranges are created because of gdal_calc's processing limit of 26 rasters (A-Z).
years = range(1995, 2051)
periods15 = [years[:15], years[15:30], years[-30:-15], years[-15:]]
periods30 = [years[:30], years[-30:]]

# Set variables of interest
variables = ['omega_arag', 'pCO2', 'pH_ROMS', 'salt', 'temp']  # from original netCDF file

# Expressions for gdal_calc
avg1year = '((A + B + C + D + E + F + G + H + I + J + K + L) / 12)'  # mean of twelve months
avg15years = '((A + B + C + D + E + F + G + H + I + J + K + L + M + N + O) / 15)'  # mean of fifteen annual averages
avg30years = '((A + B) / 2)'  # mean of two 15-year averages
avg30yearsDiff = '(B - A)'  # difference between two 30-year averages

# First calculate yearly averages, 15-year averages, 30-year averages, and then calculate 30-year average differentials
for variable in variables:

    # Calculate yearly averages
    for year in years:
        in_file = in_dir + variable + '_avg_' + str(year) + '_extracted.tif'
        output = out_dir + variable + '_1yrAvg_' + str(year) + '.tif'
        gdal_calc.Calc(calc=avg1year,
                       A=in_file, A_band=1, B=in_file, B_band=2, C=in_file, C_band=3, D=in_file, D_band=4,
                       E=in_file, E_band=5, F=in_file, F_band=6, G=in_file, G_band=7, H=in_file, H_band=8,
                       I=in_file, I_band=9, J=in_file, J_band=10, K=in_file, K_band=11, L=in_file, L_band=12,
                       outfile=output, format='GTiff', NoDataValue=None)

    # Calculate 15-year averages
    out_files15 = []
    for period in periods15:
        years15 = period
        in_files = [out_dir + variable + '_1yrAvg_' + str(year) + '.tif' for year in years15]
        output = out_dir + variable + '_15yrAvg_' + str(years15[0]) + '-' + str(years15[-1]) + '.tif'
        gdal_calc.Calc(calc=avg15years,
                       A=in_files[0], B=in_files[1], C=in_files[2], D=in_files[3],
                       E=in_files[4], F=in_files[5], G=in_files[6], H=in_files[7],
                       I=in_files[8], J=in_files[9], K=in_files[10], L=in_files[11],
                       M=in_files[12], N=in_files[13], O=in_files[14],
                       outfile=output, format='GTiff', NoDataValue=None)
        out_files15.append(output)

    # Calculate 30-year averages
    in_files = [out_dir + variable + '_15yrAvg_1995-2009.tif', out_dir + variable + '_15yrAvg_2010-2024.tif',
                out_dir + variable + '_15yrAvg_2021-2035.tif', out_dir + variable + '_15yrAvg_2036-2050.tif']
    output1 = out_dir + variable + '_30yrAvg_1995-2024.tif'
    output2 = out_dir + variable + '_30yrAvg_2021-2050.tif'
    gdal_calc.Calc(calc=avg30years,
                   A=in_files[0], B=in_files[1],
                   outfile=output1, format='GTiff', NoDataValue=None)
    gdal_calc.Calc(calc=avg30years,
                   A=in_files[2], B=in_files[3],
                   outfile=output2, format='GTiff', NoDataValue=None)

    # Calculate difference between 30-year averages
    in_files30 = [out_dir + variable + '_30yrAvg_1995-2024.tif',
                  out_dir + variable + '_30yrAvg_2021-2050.tif']
    output30yrDiff = out_dir + variable + '_30yrAvgDiff_1995-2024_vs_2021-2050.tif'
    gdal_calc.Calc(calc=avg30yearsDiff,
                   A=in_files30[0], B=in_files30[1],
                   outfile=output30yrDiff, format='GTiff', NoDataValue=None)
