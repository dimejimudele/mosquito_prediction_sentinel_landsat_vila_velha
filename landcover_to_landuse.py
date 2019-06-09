from osgeo import gdal 
import numpy as np 
from osgeo import osr
import matplotlib.pyplot as plt

#Input classification map
data_loc = (r'C:\\Users\\mudel\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\classification_map_vila_velha\\'
            r'vilavelha_classification_map.tif')

class_map = gdal.Open(data_loc)
class_mat = class_map.ReadAsArray().astype(np.float)

i, j = np.where(class_mat == 0)
class_mat[i, j] = np.nan

"""
plt.imshow(class_mat)
plt.show()
"""

def landuse_window(image, window_size):
    
    assert  (window_size% 2) == 1, "Window size must be an odd number. i.e 3,5,7.. etc"
    
    import math
    diameter = math.floor(window_size / 2)                    #To move the window around boundary pixels
    image_pad = np.pad(image, diameter, 'reflect')
    land_use_map_pad = np.zeros(image_pad.shape)
    max_row, max_col = image.shape
    for i in range(diameter, max_row - diameter + 1):
        for j in range(diameter, max_col - diameter + 1):
            image_window = image_pad[i - diameter: (i + diameter + 1), j - diameter: (j + diameter + 1)]
            center_class = image_pad[i, j]
            if center_class == np.nan:
                continue
            else: 
                class_count = (image_window == image_pad[i, j]).sum()
                land_use_map_pad[i, j] = ((image_pad[i, j] * 100) + ((class_count/(window_size** 2)) * 100)) - 1

    land_use_map = land_use_map_pad[diameter : diameter + max_row, diameter : diameter + max_col]
    i, j = np.where(land_use_map == 0)
    land_use_map[i, j] = np.nan
    return land_use_map
land_use = landuse_window(class_mat, window_size = 21)
"""
plt.imshow(land_use)
plt.colorbar()
plt.show()
"""
def array2raster(newRasterfn, dataset, array, dtype):
    """
    save GTiff file from numpy.array
    input:
        newRasterfn: name to save file with
        dataset : original tif file to obtain geo information. You should use the Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)
        array : The Land surface temperature array
        dtype: Byte or Float32.
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX, pixelWidth, b, originY, d, pixelHeight = dataset.GetGeoTransform()

    driver = gdal.GetDriverByName('GTiff')

    # set data type to save.
    GDT_dtype = gdal.GDT_Unknown
    if dtype == "Byte":
        GDT_dtype = gdal.GDT_Byte
    elif dtype == "Float32":
        GDT_dtype = gdal.GDT_Float32
    else:
        print("Not supported data type.")

    # set number of band.
    if array.ndim == 2:
        band_num = 1
    else:
        band_num = array.shape[2]

    outRaster = driver.Create(newRasterfn, cols, rows, band_num, GDT_dtype)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    # Loop over all bands.
    for b in range(band_num):
        outband = outRaster.GetRasterBand(b + 1)
        # Read in the band's data into the third dimension of our array
        if band_num == 1:
            outband.WriteArray(array)
        else:
            outband.WriteArray(array[:,:,b])

    # setteing srs from input tif file.
    prj=dataset.GetProjection()
    outRasterSRS = osr.SpatialReference(wkt=prj)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

data_out_loc = (r'C:\\Users\\mudel\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\classification_map_vila_velha\\'
            r'vilavelha_land_use_map_window_21.tif')
array2raster(data_out_loc, class_map, land_use, 'Float32' )