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