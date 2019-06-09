import os #, fnmatch

os.environ['GDAL_DATA'] = 'C:\\Users\\mudel\\Anaconda3\\Lib\\site-packages\\osgeo\\data\\gdal'
#os.environ['PROJ_LIB'] = os.environ['CONDA_PREFIX'] + r'\Library\share'

input_data = "C:\\Users\\mudel\\Documents\\2018_2019_PhD\\gdal_warp_translate\\2018_lst\\LST_day.tif"


#directory_in_str = r"C:\\Users\\mudel\\Documents\\Test_Interpolation_MOD09A1\\full\\NDVI_NDWI_MOD09A1_500m_batch1\\"

for a in range(1,36):
    output_data = "C:\\Users\\mudel\\Documents\\2018_2019_PhD\\gdal_warp_translate\\2018_lst\\day\\" + str(a) + ".tif"
    cmd = 'gdal_translate %s -b %s %s' %(input_data,a,output_data)
    os.system(cmd)


