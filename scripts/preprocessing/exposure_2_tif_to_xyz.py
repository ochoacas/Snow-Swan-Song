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