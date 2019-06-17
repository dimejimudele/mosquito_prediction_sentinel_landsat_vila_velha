import numpy as np
import pandas as pd 
from osgeo import gdal
import numpy as np
from os import listdir
from os.path import isfile, join
from osgeo import osr
import matplotlib.pyplot as plt
import random
import math

#EO Data directory
class_map_data_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\classification_map_vila_velha\\'
            r'vilavelha_classification_map.tif')

landuse_map_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\classification_map_vila_velha\\'
            r'vilavelha_land_use_mask70_window_7.tif')

lst_directory = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                r'mosquito_pop_landsat_Sentinel\\LST_landsat_2017_vilavelha\\time_series\\')

ndvi_directory = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                r'mosquito_pop_landsat_Sentinel\\ndvi_sentinel_2017_vilavelha\\time_series\\')

ndwi_directory = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                r'mosquito_pop_landsat_Sentinel\\ndwi_sentinel_2017_vilavelha\\time_series\\')

"""
Input classification map and land use map
"""
class_map = gdal.Open(class_map_data_loc)
class_mat = class_map.ReadAsArray()
size_class = class_mat.shape


land_use_map = gdal.Open(landuse_map_loc)
land_use_mask = land_use_map.ReadAsArray()
size_landuse = land_use_mask.shape

assert size_class == size_landuse,"Classification and land use maps must be of equal shape" 

"""
Create 3D matrics of time series of images
"""
#Create tensor of input LST stack
lst_files = [lst_directory + '\\' + f for f in listdir(lst_directory) if isfile(join(lst_directory, f))]
no_of_lst_images = len(lst_files)
stack_lst = np.zeros((no_of_lst_images, size_class[0], size_class[1]))

for idx, img in enumerate(lst_files): 
    lst_image = gdal.Open(lst_files[idx])
    lst_array = lst_image.ReadAsArray()
    assert lst_array.shape == size_class, "Input LST data does not fit Tensor dimension"
    stack_lst[idx,:,:] = lst_array

#Create tensor of input NDVI stack
ndvi_files = [ndvi_directory + '\\' + f for f in listdir(ndvi_directory) if isfile(join(ndvi_directory, f))]
no_of_ndvi_images = len(ndvi_files)
stack_ndvi = np.zeros((no_of_ndvi_images,size_class[0], size_class[1]))

for idx, img in enumerate(ndvi_files): 
    ndvi_image = gdal.Open(ndvi_files[idx])
    ndvi_array = ndvi_image.ReadAsArray()
    assert ndvi_array.shape == size_class, "Input ndvi data does not fit Tensor dimension"
    stack_ndvi[idx,:,:] = ndvi_array

#Create tensor of input NDWI stack
ndwi_files = [ndwi_directory + '\\' + f for f in listdir(ndwi_directory) if isfile(join(ndwi_directory, f))]
no_of_ndwi_images = len(ndwi_files)
stack_ndwi = np.zeros((no_of_ndwi_images, size_class[0], size_class[1]))

for idx, img in enumerate(ndwi_files): 
    ndwi_image = gdal.Open(ndwi_files[idx])
    ndwi_array = ndwi_image.ReadAsArray()
    assert ndwi_array.shape == size_class, "Input ndwi data does not fit Tensor dimension"
    stack_ndwi[idx,:,:] = ndwi_array


"""
Select pixels with at least 70% cloud across the observation time
"""
#LST
percent_cloud_75_lst = np.zeros(size_class)
for i in range(stack_lst.shape[1]):
    for j in range(stack_lst.shape[2]):
        not_nan = np.count_nonzero(~np.isnan(stack_lst[:,i,j]))
        if (not_nan >= np.floor(0.70 * no_of_lst_images)) & (land_use_mask[i, j] == 1):
           percent_cloud_75_lst[i,j] = 1

#NDVI
percent_cloud_75_ndvi = np.zeros(size_class)
for i in range(stack_ndvi.shape[1]):
    for j in range(stack_ndvi.shape[2]):
        not_nan = np.count_nonzero(~np.isnan(stack_ndvi[:,i,j]))
        if (not_nan >= np.floor(0.70 * no_of_ndvi_images)) & (land_use_mask[i, j] == 1):
           percent_cloud_75_ndvi[i,j] = 1

#NDWI
percent_cloud_75_ndwi = np.zeros(size_class)
for i in range(stack_ndwi.shape[1]):
    for j in range(stack_ndwi.shape[2]):
        not_nan = np.count_nonzero(~np.isnan(stack_ndwi[:,i,j]))
        if (not_nan >= np.floor(0.70 * no_of_ndwi_images)) & (land_use_mask[i, j] == 1):
           percent_cloud_75_ndwi[i,j] = 1


"""
Assign class label to selected pixels 
"""
a, b = np.where(percent_cloud_75_lst == 1)
percent_cloud_75_lst[a,b] = class_mat[a,b] 

a, b = np.where(percent_cloud_75_ndvi == 1)
percent_cloud_75_ndvi[a,b] = class_mat[a,b] 

a, b = np.where(percent_cloud_75_ndwi == 1)
percent_cloud_75_ndwi[a, b] = class_mat[a, b] 
#print((percent_cloud_75_ndwi == 2).sum(), 'Tall veg NDWI pixels')


"""
Extract samples LST
"""
def extract_samples(percent_cloud_select, class_label, threeD_stack):
        l, m = np.where(percent_cloud_select == class_label)
        mapIndexPosition = list(zip(l, m))
        random.shuffle(mapIndexPosition)
        l, m = zip(*mapIndexPosition)

        #Training LST
        train_sample_size = int(math.ceil((len(l))/2))
        mat_train_feature = np.zeros((no_of_lst_images, train_sample_size))
        for x in range(train_sample_size):
                train_pixel_series = threeD_stack[:, l[x], m[x]]
                mat_train_feature[:,x] = train_pixel_series
        train_feature = np.nanmean(mat_train_feature, axis=1)
        train_feature_std = np.nanstd(mat_train_feature, axis=1)

        #Validation LST
        test_start = train_sample_size + 1
        l = l[test_start:]
        m = m[test_start:]
        test_sample_size = len(l)
        mat_test_feature = np.zeros((no_of_lst_images, test_sample_size))
        for x in range(test_sample_size):
                #idx = x - second_half_length
                test_pixel_series = threeD_stack[:, l[x], m[x]]
                mat_test_feature[:,x] = test_pixel_series   
        test_feature = np.nanmean(mat_test_feature, axis=1)
        test_feature_std = np.nanstd(mat_test_feature, axis=1)

        return train_feature, test_feature, train_feature_std, test_feature_std

"""
sv: Short vegetation
tv: tall vegetation
as: Artificial surface
bs: Bare soil
w: water
"""
train_lst_sv, test_lst_sv, train_lst_sv_std, test_lst_sv_std = extract_samples(percent_cloud_select = percent_cloud_75_lst, class_label = 1, threeD_stack = stack_lst)
train_lst_tv, test_lst_tv, train_lst_tv_std, test_lst_tv_std  = extract_samples(percent_cloud_select = percent_cloud_75_lst, class_label = 2, threeD_stack = stack_lst)
train_lst_as, test_lst_as, train_lst_as_std, test_lst_as_std  = extract_samples(percent_cloud_select = percent_cloud_75_lst, class_label = 3, threeD_stack = stack_lst)
train_lst_bs, test_lst_bs, train_lst_bs_std, test_lst_bs_std  = extract_samples(percent_cloud_select = percent_cloud_75_lst, class_label = 4, threeD_stack = stack_lst)
train_lst_w, test_lst_w, train_lst_w_std, test_lst_w_std  = extract_samples(percent_cloud_select = percent_cloud_75_lst, class_label = 5, threeD_stack = stack_lst)

weeks_landsat_lst = [15, 16, 17, 19, 21, 24, 25, 26, 27, 29, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 47, 48, 52]

print(len(train_lst_sv))
print(len(train_lst_w))
df_lst_train = pd.DataFrame({
        'year_week': weeks_landsat_lst,
        'lst_sv': train_lst_sv,
        'lst_tv': train_lst_tv,
        'lst_as': train_lst_as,
        'lst_bs': train_lst_bs,
        'lst_w': train_lst_w
        })

df_lst_test = pd.DataFrame({
        'year_week': weeks_landsat_lst,
        'lst_sv': test_lst_sv,
        'lst_tv': test_lst_tv,
        'lst_as': test_lst_as,
        'lst_bs': test_lst_bs,
        'lst_w': test_lst_w
        })

lst_train_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'lst_train.csv')

lst_test_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'lst_test.csv')

df_lst_train.to_csv(lst_train_loc)
df_lst_test.to_csv(lst_test_loc)


df_lst_train_std = pd.DataFrame({
        'year_week': weeks_landsat_lst,
        'lst_sv': train_lst_sv_std,
        'lst_tv': train_lst_tv_std,
        'lst_as': train_lst_as_std,
        'lst_bs': train_lst_bs_std,
        'lst_w': train_lst_w_std
        })

df_lst_test_std = pd.DataFrame({
        'year_week': weeks_landsat_lst,
        'lst_sv': test_lst_sv_std,
        'lst_tv': test_lst_tv_std,
        'lst_as': test_lst_as_std,
        'lst_bs': test_lst_bs_std,
        'lst_w': test_lst_w_std
        })

lst_train_loc_std = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'lst_train_std_error.csv')

lst_test_loc_std = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'lst_test_std_error.csv')

df_lst_train_std.to_csv(lst_train_loc_std)
df_lst_test_std.to_csv(lst_test_loc_std)

#NDVI NDWI 
train_ndvi_sv, test_ndvi_sv, train_ndvi_sv_std, test_ndvi_sv_std = extract_samples(percent_cloud_select = percent_cloud_75_ndvi, class_label = 1, threeD_stack = stack_ndvi)
train_ndvi_tv, test_ndvi_tv, train_ndvi_tv_std, test_ndvi_tv_std = extract_samples(percent_cloud_select = percent_cloud_75_ndvi, class_label = 2, threeD_stack = stack_ndvi)
train_ndvi_as, test_ndvi_as, train_ndvi_as_std, test_ndvi_as_std = extract_samples(percent_cloud_select = percent_cloud_75_ndvi, class_label = 3, threeD_stack = stack_ndvi)
train_ndvi_bs, test_ndvi_bs, train_ndvi_bs_std, test_ndvi_bs_std = extract_samples(percent_cloud_select = percent_cloud_75_ndvi, class_label = 4, threeD_stack = stack_ndvi)
train_ndvi_w, test_ndvi_w, train_ndvi_w_std, test_ndvi_w_std = extract_samples(percent_cloud_select = percent_cloud_75_ndvi, class_label = 5, threeD_stack = stack_ndvi)

train_ndwi_sv, test_ndwi_sv, train_ndwi_sv_std, test_ndwi_sv_std = extract_samples(percent_cloud_select = percent_cloud_75_ndwi, class_label = 1, threeD_stack = stack_ndwi)
train_ndwi_tv, test_ndwi_tv, train_ndwi_tv_std, test_ndwi_tv_std = extract_samples(percent_cloud_select = percent_cloud_75_ndwi, class_label = 2, threeD_stack = stack_ndwi)
train_ndwi_as, test_ndwi_as, train_ndwi_as_std, test_ndwi_as_std = extract_samples(percent_cloud_select = percent_cloud_75_ndwi, class_label = 3, threeD_stack = stack_ndwi)
train_ndwi_bs, test_ndwi_bs, train_ndwi_bs_std, test_ndwi_bs_std = extract_samples(percent_cloud_select = percent_cloud_75_ndwi, class_label = 4, threeD_stack = stack_ndwi)
train_ndwi_w, test_ndwi_w, train_ndwi_w_std, test_ndwi_w_std = extract_samples(percent_cloud_select = percent_cloud_75_ndwi, class_label = 5, threeD_stack = stack_ndwi)
weeks_sentinel = [14, 17, 20, 23, 26, 28, 29, 30, 31, 33, 34, 36, 37, 39, 40, 42, 43, 45, 46, 48, 49, 50, 51, 52]

df_ndvi_ndwi_train = pd.DataFrame({
        'year_week': weeks_sentinel,
        'ndvi_sv': train_ndvi_sv,
        'ndvi_tv': train_ndvi_tv,
        'ndvi_as': train_ndvi_as,
        'ndvi_bs': train_ndvi_bs,
        'ndvi_w': train_ndvi_w,
        'ndwi_sv': train_ndwi_sv,
        'ndwi_tv': train_ndwi_tv,
        'ndwi_as': train_ndwi_as,
        'ndwi_bs': train_ndwi_bs,
        'ndwi_w': train_ndwi_w
        })

df_ndvi_ndwi_test = pd.DataFrame({
        'year_week': weeks_sentinel,
        'ndvi_sv': test_ndvi_sv,
        'ndvi_tv': test_ndvi_tv,
        'ndvi_as': test_ndvi_as,
        'ndvi_bs': test_ndvi_bs,
        'ndvi_w': test_ndvi_w,
        'ndwi_sv': test_ndwi_sv,
        'ndwi_tv': test_ndwi_tv,
        'ndwi_as': test_ndwi_as,
        'ndwi_bs': test_ndwi_bs,
        'ndwi_w': test_ndwi_w
        })

df_ndvi_ndwi_train_std = pd.DataFrame({
        'year_week': weeks_sentinel,
        'ndvi_sv': train_ndvi_sv_std,
        'ndvi_tv': train_ndvi_tv_std,
        'ndvi_as': train_ndvi_as_std,
        'ndvi_bs': train_ndvi_bs_std,
        'ndvi_w': train_ndvi_w_std,
        'ndwi_sv': train_ndwi_sv_std,
        'ndwi_tv': train_ndwi_tv_std,
        'ndwi_as': train_ndwi_as_std,
        'ndwi_bs': train_ndwi_bs_std,
        'ndwi_w': train_ndwi_w_std
        })

df_ndvi_ndwi_test_std = pd.DataFrame({
        'year_week': weeks_sentinel,
        'ndvi_sv': test_ndvi_sv_std,
        'ndvi_tv': test_ndvi_tv_std,
        'ndvi_as': test_ndvi_as_std,
        'ndvi_bs': test_ndvi_bs_std,
        'ndvi_w': test_ndvi_w_std,
        'ndwi_sv': test_ndwi_sv_std,
        'ndwi_tv': test_ndwi_tv_std,
        'ndwi_as': test_ndwi_as_std,
        'ndwi_bs': test_ndwi_bs_std,
        'ndwi_w': test_ndwi_w_std
        })

ndvi_ndwi_train_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'ndvi_ndwi_train.csv')

ndvi_ndwi_test_loc = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'ndvi_ndwi_test.csv')

df_ndvi_ndwi_train.to_csv(ndvi_ndwi_train_loc)
df_ndvi_ndwi_test.to_csv(ndvi_ndwi_test_loc)

ndvi_ndwi_train_loc_std = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'ndvi_ndwi_train_std_error.csv')

ndvi_ndwi_test_loc_std = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
            r'mosquito_pop_landsat_Sentinel\\'
            r'ndvi_ndwi_test_std_error.csv')

df_ndvi_ndwi_train_std.to_csv(ndvi_ndwi_train_loc_std)
df_ndvi_ndwi_test_std.to_csv(ndvi_ndwi_test_loc_std)

"""
c, d = np.where(percent_cloud_75_ndvi == 1)
percent_cloud_75_ndvi[c,d] = class_mat[c,d]

e, f = np.where(percent_cloud_75_ndwi == 1)
percent_cloud_75_ndwi[e,f] = class_mat[e,f]



i, j = np.where(percent_cloud_75_lst == 1)

percent_cloud_75_lst[i, j] = class_mat[i,j] 


short_vegn = (percent_cloud_75_lst == 1).sum()
tall_vegn = (percent_cloud_75_lst == 2).sum()
artificialn = (percent_cloud_75_lst == 3).sum()
baresoiln = (percent_cloud_75_lst == 4).sum()
watern = (percent_cloud_75_lst == 5).sum()

print(short_vegn, tall_vegn, artificialn, baresoiln, watern)
"""