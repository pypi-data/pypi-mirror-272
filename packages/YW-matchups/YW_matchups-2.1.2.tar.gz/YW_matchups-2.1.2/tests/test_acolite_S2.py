# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import YW_matchups








# sat_file = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER/test_output_S2_60m.nc'


# sat_folder = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER'

sat_folder = '/Volumes/San2T/GLORIA/ACed/S2_Tmart_ACOLITE/S2A_MSIL1C_20150912T101403_N0204_R022_T32TPR_20150912T101724'
sat_folder = '/Users/yw/Downloads'



is_file = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER/test_in_situ.csv'
out_file = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER/test_out.csv'


test = YW_matchups.run(sat_folder, is_file, AC='ACOLITE', out_file=out_file, to_log = True)




'''
# Plot 

from matplotlib import pyplot as plt
plt.imshow(test3, interpolation='nearest')
plt.show()

'''

