import matplotlib.pyplot as plt 
import pandas as pd 
plt.style.use('seaborn')

lst_train = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\lst_train_spline.csv'))


ndvi_ndwi_train = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\ndvi_ndwi_train_spline.csv'))

lst_error = pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\lst_train_std_error.csv'))

ndvi_ndwi_error= pd.read_csv((r'C:\\Users\\mudel\\OneDrive - Università di Pavia\\'
                            r'2018_2019_PhD\\Information Theory for Big data UFAL 2019\\'
                                r'mosquito_pop_landsat_Sentinel\\time_series_csv\\ndvi_ndwi_train_std_error.csv'))

week_numbers = ndvi_ndwi_train['year_week']
header_lst = lst_train.columns.values.tolist()[1:]
header_ndvi = ndvi_ndwi_train.columns.values.tolist()[1:6]
header_ndwi = ndvi_ndwi_train.columns.values.tolist()[6:11]
legend = ['short vegetation','Tall vegetation', 'Urban surface', 'Baresoil', 'Water']

data_ndvi = ndvi_ndwi_train[header_ndvi]
error_ndvi = ndvi_ndwi_error[header_ndvi]

data_ndwi = ndvi_ndwi_train[header_ndwi]
error_ndwi = ndvi_ndwi_error[header_ndwi]

def plot_data(data_input, error_input, header, title, variable, legend):
    plt.figure()
    for x in header:
        plt.errorbar(x = week_numbers, y = data_input[x], yerr=error_input[x],  marker = 'o')
    plt.ylabel(variable)
    plt.xlabel('week of the year')
    plt.title(title)
    plt.legend(legend)
    plt.show()

plot_data(lst_train, lst_error, header_lst, 'LST - Landsat 8: Training', 'LST', legend)
plot_data(data_ndvi, error_ndvi, header_ndvi, 'NDVI - Sentinel 2: Training', 'NDVI', legend)
plot_data(data_ndwi, error_ndwi, header_ndwi, 'NDWI - Sentinel 2: Training', 'NDWI', legend)