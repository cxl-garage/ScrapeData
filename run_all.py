"""
Script to run through each subdirectory and execute run_tf_detector_batch.py on
images to create .json files

Author: Henrik Cox
Date: 01/31/2020
"""

import os
import GBIFscrape as scrape
import numpy as np
#begin_path = "cd /home/cxl_garage/Desktop/CameraTraps"
#os.system(begin_path)

#data_directory = "CameraTraps"
#directory_list = os.listdir(data_directory)
#print(len(directory_list))
#folders = set([])

def example():
    print('Finding Indexes')
    classfilter_index = scrape.Filter('test_GBIF_Scrape.zip', 100, 'genus', 'Oreochromis', '3', '1', '0', '0')
    user_class_name = 'class1'
    #dtype1 = np.dtype([('gender', '|S1'), ('height', 'f8')])
    print('creating actual array')
    a = np.loadtxt('test_GBIF_Scrape/multimedia.txt', dtype = str, skiprows=1, usecols=(3))
    a = np.extract(classfilter_index,a)
    b = np.full(len(a),user_class_name,dtype=('U', 10))
    class_array = np.stack((b,a), axis=-1)
    print('Array Complete')
    return class_array

def get_folders(directory):
    folders = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if root not in folders:
                folders.append(root)
    #print(folders)
    return folders

def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def get_orderName(directory):
    order = str(directory)
    #print(str(directory))
    #print(order)
    start = order.rfind('/') + 1
    #print(start)
    #print(order[start:])
    #print(order)
    return order[start:]

data_array = example()
#First coluimn is the user-inputted class - this will be the seocnd megadector batch input ({.json})
#print(data_array[:,0])
#Second column is the list of jpg file paths (to their web browser address) - this will be the first megadetector batch input (image_file_path.jpg)
#print(data_array[:,1])



all_folders = get_folders('/home/cxl_garage/Desktop/CameraTraps/Animal_photos')
#collect numpy array for links on backend instead of get_folders (which is local work)!!!!
#print(len(all_folders))
for i in all_folders:
    #print(i)
    order_name = get_orderName(i)
    #print(order_name)
    #megadetect_batch = "python3 run_tf_detector_batch.py megadetector_v3.pb {} {}.json".format(i, order_name)
    megadetect_batch = "python3 run_tf_detector_batch.py megadetector_v3.pb {} {}.json".format(data_array[:,1], data_array[:,0])
    #first input is going to be the links from a numpy array!!!!
        #megadetect_batch = "python3 run_tf_detector_batch.py megadetector_v3.pb %s %s.json" % (i), (order_name)
    print(megadetect_batch)
    os.system(megadetect_batch)

full_file_paths = get_filepaths('/home/cxl_garage/Desktop/CameraTraps/Animal_photos')
#print("Total number of images is = ", len(full_file_paths))
