import pandas as pd 
import numpy as np 
import scipy as sp

lst_train = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\lst_train.csv'))

lst_test = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\lst_test.csv'))


ndvi_ndwi_train = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\ndvi_ndwi_train.csv'))

ndvi_ndwi_test = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\ndvi_ndwi_test.csv'))

lst_train_out = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\lst_train_spline.csv')

lst_test_out = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\lst_test_spline.csv')


ndvi_ndwi_train_out = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\ndvi_ndwi_train_spline.csv')

ndvi_ndwi_test_out = (r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\ndvi_ndwi_test_spline.csv')

lst_train_spl = lst_train.astype(float).interpolate(method='slinear', limit_direction = 'forward')
lst_test_spl = lst_test.astype(float).interpolate(method='slinear', limit_direction = 'forward')


ndvi_ndwi_train_spl = ndvi_ndwi_train.astype(float).interpolate(method='slinear', limit_direction = 'forward')
ndvi_ndwi_test_spl = ndvi_ndwi_test.astype(float).interpolate(method='slinear', limit_direction = 'forward')

lst_train_spl.to_csv(lst_train_out)
lst_test_spl.to_csv(lst_test_out)

ndvi_ndwi_train_spl.to_csv(ndvi_ndwi_train_out)
ndvi_ndwi_test_spl.to_csv(ndvi_ndwi_test_out)