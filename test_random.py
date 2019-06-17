import numpy as np 

"""
mat = np.random.randn(5, 4)

a, b = np.where(mat > -0.5)
print(mat)
print(a)
print(b)

import random
mapIndexPosition = list(zip(a, b))
random.shuffle(mapIndexPosition)
a, b = zip(*mapIndexPosition)
print(a)
print(b)
"""
"""
a = np.array([[1, 2, 1], [3, 4, 1]])
print(a)
b = np.mean(a, axis=0)
print(b)
"""
import numpy as np
a = [x for x in range(13)]
half = int(np.ceil(len(a)/2))
print(a)
print(a[:half])
o_half = half  + 1
print(a[o_half:])
"""
import math
b = 5
a = math.ceil(b/2)
print(a)
"""


"""
################################################
######                  SHORT VEGETATION - LST
################################################
l, m = np.where(percent_cloud_75_lst == 2)
mapIndexPosition = list(zip(l, m))
random.shuffle(mapIndexPosition)
l, m = zip(*mapIndexPosition)

print(len(l))
#Training LST
train_sample_size = math.ceil((len(l))/2)
lst_mat_train_sv = np.zeros((no_of_lst_images, train_sample_size))
for x in range(train_sample_size):
        lst_pixel_series = stack_lst[:, l[x], m[x]]
        lst_mat_train_sv[:,x] = lst_pixel_series
lst_train_sv = np.nanmean(lst_mat_train_sv, axis=0)

#Validation LST
test_start = train_sample_size + 1
l = l[test_start:]
m = m[test_start:]
test_sample_size = len(l)
lst_mat_val_sv = np.zeros((no_of_lst_images, test_sample_size))

print(len(l))
for x in range(test_sample_size):
        #idx = x - second_half_length
        lst_pixel_series = stack_lst[:, l[x], m[x]]
        lst_mat_val_sv[:,x] = lst_pixel_series   
lst_val_sv = np.nanmean(lst_mat_val_sv, axis=0)

print(lst_train_sv, lst_val_sv)
"""