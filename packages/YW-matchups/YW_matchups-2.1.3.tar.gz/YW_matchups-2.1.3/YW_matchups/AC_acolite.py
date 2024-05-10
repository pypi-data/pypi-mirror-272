


# Tool package for ACOLITE


import netCDF4 as nc4
import ast
import numpy as np
import datetime as dt



# Get datetime object 
def get_datetime(sat_file):
    with nc4.Dataset(sat_file,"r") as nc:
        
        sensor = nc.getncattr('sensor')

        
        ### full resolution ###
        # datetime_sat_string = nc.getncattr('isodate')
        # format_string = '%Y-%m-%dT%H:%M:%S.%f%z'
        
        # March 20, 2024 update: prioritize inputfile name instead
        
        try: 
            
            if sensor=='L8_OLI': raise Exception()
            
            inputfile = nc.getncattr('inputfile').split('/')[-1]
            datetime_sat_string = inputfile[11:26]
            format_string = '%Y%m%dT%H%M%S'
            
        except:
            # nearest second 
            datetime_sat_string = nc.getncattr('isodate').split('.', 1)[0]
            format_string = '%Y-%m-%dT%H:%M:%S'
            
        datetime_sat_obj = dt.datetime.strptime(datetime_sat_string, format_string)
    return [datetime_sat_obj, False]
    
    

# Read NC data 

def read_file(sat_file, ACOLITE_L2R):
    
    with nc4.Dataset(sat_file,"r") as nc:
        sensor = nc.getncattr('sensor')
        
        # S2 wavelengths 
        if sensor == 'S2A_MSI' or sensor == 'S2B_MSI':
            column_names = ['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12']
        
            if sensor == 'S2A_MSI':
                bands = [443,492,560,665,704,740,783,833,865,1614,2202] 
            elif sensor == 'S2B_MSI':
                bands = [442,492,559,665,704,739,780,833,864,1610,2186]
        
        # L8 wavelengths
        elif sensor == 'L8_OLI':
            bands = [443, 483, 561, 655, 865, 1609, 2201]
            column_names = ['B1','B2','B3','B4','B5','B6','B7']
        
        # band names for extracting values
        if ACOLITE_L2R: 
            band_names = ['rhos_' + str(item) for item in bands]
        else: 
            band_names = ['rhow_' + str(item) for item in bands]

        # dimension
        global_dims = nc.getncattr('global_dims')
        # YW: I'm not sure about 0 and 1, but both S2 and PRISMA have square images
        height = global_dims[0] # equivalent to 'lines' before 
        width = global_dims[1]  # equivalent to 'pixels' before 

        # latlon
        lat = nc.variables['lat'][:,:]
        lon = nc.variables['lon'][:,:]

        # to store data
        rhow_data = np.ma.empty([len(bands),int(height),int(width)])

        for k in range(len(bands)):
            varname = band_names[k]
            rhow_data[k] = nc.variables[varname][:,:]
            
        # remove non-water pixels in L2R mode 
        if ACOLITE_L2R: 
            # 1600 nm band 
            index_1600 = min(range(len(bands)), key=lambda i: abs(bands[i] - 1600))
            
            # non-water mask 
            my_mask = rhow_data[index_1600] > 0.0215
            rhow_data[:, my_mask] = np.nan

    return {'bands': band_names,            # variable names of the bands 
            'sensor': sensor,
            'column_names': column_names,   # column names for final output
            'width': width,                 # width of the data array
            'height': height,               # height of the data array
            'lat': lat,                     # 2d data array: latitude at [y,x]
            'lon': lon,                     # 2d data array: longitude at [y,x]
            'rhow_data': rhow_data}         # 3d data array: reflectance at [band, y, x]





















