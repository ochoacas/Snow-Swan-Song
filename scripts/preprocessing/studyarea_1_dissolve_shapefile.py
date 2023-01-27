from qgis.core import QgsApplication, QgsProcessingFeedback
from osgeo import ogr, osr
import sys

QgsApplication.setPrefixPath(r'C:\\OSGeo4W64\\apps\\qgis-dev', True)
qgs = QgsApplication([], False)
qgs.initQgis()

sys.path.append(r'C:\\OSGeo4W64\\apps\\qgis-ltr\python\plugins')
from processing.core import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
feedback = QgsProcessingFeedback()

driver = ogr.GetDriverByName('ESRI Shapefile')

layer = QgsVectorLayer("boundaries\\WBDHU8.shp", "WBDHU8", "ogr")
if not layer.isValid():
    print("Layer failed to load!")

processing.dissolve(layer, "WBDHU8_dissolved.shp", onlySelectedFeatures=False, uniqueIdField=-1, p=None)
