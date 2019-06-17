import os #, fnmatch

os.environ['GDAL_DATA'] = 'C:\\Users\\mudel\\Anaconda3\\Lib\\site-packages\\osgeo\\data\\gdal'
#os.environ['PROJ_LIB'] = os.environ['CONDA_PREFIX'] + r'\Library\share'

input_data = (r'C:\\Users\\mudel\\Documents\\'
                r'2018_2019_PhD\\gdal_warp_translate\\'
                r'ndwi_sentinel_2017_vilavelha\\NDWI_image_time_series_sentinel.tif')


#directory_in_str = r"C:\\Users\\mudel\\Documents\\Test_Interpolation_MOD09A1\\full\\NDVI_NDWI_MOD09A1_500m_batch1\\"

for a in range(20,21):
    output_data = "C:\\Users\\mudel\\Documents\\2018_2019_PhD\\gdal_warp_translate\\ndwi_sentinel_2017_vilavelha\\time_series\\" + str(a) + ".tif"
    cmd = 'gdal_translate %s -b %s %s' %(input_data,a,output_data)
    os.system(cmd)


