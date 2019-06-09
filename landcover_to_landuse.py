from osgeo import gdal 
import numpy as np 
import matplotlib.pyplot as plt


data_loc = (r'C:\\Users\\mudel\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\classification_map_vila_velha\\'
            r'vilavelha_classification_map.tif')

class_map = gdal.Open(data_loc)
class_mat = class_map.ReadAsArray().astype(np.float)
plt.imshow(class_mat)
plt.colorbar()
plt.show()

