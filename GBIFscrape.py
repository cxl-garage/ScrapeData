## Customized Data Scrape from GBIF

## Dependencies
# pip install python-dwca-reader
# pip install pandas
# pip install seaborn


## Assumptions of this Script
# Will only be searching for: animal images by human/machine observation in GBIF database,


## Things to consider


####### LIBRARIES #######
from dwca.read import DwCAReader
from dwca.darwincore.utils import qualname as qn
import glob
import os
import numpy as np

####### FUNCTIONS #######

def canOpener(fileName, folderName, pictName,arrayName, first, last,):
  #only do once, as they will now be in the folders from the .csv files
  csv_filename = fileName
  placement = folderName
  a= first
  b = last
  j=0
  i=pictName + str(j)
  with open(csv_filename+".csv".format(csv_filename), 'r') as csv_file:
    for line in reader(csv_file):
      if  a<=j<=b and line[0] != '':
        urlretrieve(line[0], placement + i + ".jpg")
        img=io.imread(line[0])
        arrayName.append(img)
        print(j)
        j=j+1
        i=pictName + str(j)
        j=int(j)

      else:
        j=j+1

## Define Classes
def Filter_Loop(zipfile, max_instances, level, Phylogenic, Temporal, Length, Location, Range):
    dwca = DwCAReader(zipfile)
    #TemporalIndex = []
    new = []
    k = 0
    row = 0
    for core_row in dwca:
        #print(row)
        if k <= int(max_instances):
            #print(core_row.data[qn(level)])
            if (Phylogenic == core_row.data[qn(level)]) and (Temporal == core_row.data[qn('month')]):
                new = np.append(new, 1)
                k = k + 1
            else:
                new = np.append(new, 0)
        row = row + 1
    dwca.close
    #print('Make Month, Location/Range Optional')
    return new

def Filter_pandas(zipfile, max_instances, level, Phylogenic, Temporal, Length, Location, Range):
    import pandas as pd
    import seaborn as sns

    with DwCAReader(zipfile) as dwca:
        #print("Core data file is: {}".format(dwca.descriptor.core.file_location)) # => 'occurrence.txt'

        core_df = dwca.pd_read('occurrence.txt', parse_dates=True)

       # All Pandas functionalities are now available on the core_df DataFrame

    # Number of records for each institutioncode
    #genus = core_df['genus'].head()
    #genus = core_df['genus'].value_counts()
    new = core_df[(core_df[level] == Phylogenic)]# &
                #(core_df['month'] == Temporal)] #&
                #(core_df["decimalLongitude"] != 0.0) &
                #(core_df["decimalLongitude"].notnull()) &
                #(core_df["eventDate"].notnull())]
    new = new.index
    return new


def exampleLoop(Filter):
    if Filter == 'loop':
        classfilter_index = Filter_Loop('test_GBIF_Scrape.zip', 100, 'genus', 'Oreochromis', '3', '1', '0', '0')
        user_class_name = 'class1'
        a = np.loadtxt('test_GBIF_Scrape/multimedia.txt', dtype = str, skiprows=1, usecols=(3))
        a = np.extract(classfilter_index,a)
        b = np.full(len(a),user_class_name,dtype=('U', 10))
        class_array = np.stack((b,a), axis=-1)
    if Filter == 'pandas':
        classfilter_index = Filter_pandas('test_GBIF_Scrape.zip', 100, 'genus', 'Oreochromis', '3', '1', '0', '0')
        print(classfilter_index)
        user_class_name = 'class1'
        a = np.loadtxt('test_GBIF_Scrape/multimedia.txt', dtype = str, skiprows=1, usecols=(3))
        a = np.extract(classfilter_index,a)
        b = np.full(len(a),user_class_name,dtype=('U', 10))
        class_array = np.stack((b,a), axis=-1)
    else:
        print('Filter Type does not exist')
    return class_array

def userinput():
    userinput = 1
    while 1 :
        input_location = input('Do you want to limit by location? (y/n): ')
        if input_location == 'y':
            print('Location Limitation not functional yet...')
            Location = 0
            Range = 0
            break
        if input_location == 'n':
            print('Location Limitation OFF')
            Location = 0
            Range = 0
            break
        else:
            print('Incorrect Key Selected, please choose y or n')
    userinput = 1
    while 1 :
        input_temporal = input('Do you want to limit by month? (y/n): ')
        if input_location == 'y':
            input_month = input('Temporal Limitation ON, which month will the asset be deployed? (1-12 for months of the year): ')
            input_deployment_length = input('How long will the asset be deployed? (months): ')
            break
        if input_location == 'n':
            print('Temporal Limitation OFF: ')
            input_month = 0
            input_deployment_length = 0
            break
        else:
            print('Incorrect Key Selected, please choose y or n')

    another_class = 1
    userinput = 1
    export_array = []
    while 1:
        input_anotherclass = input('Want to add another class? y/n: ')
        if input_anotherclass == 'y':
            print('Adding another class...')
            userinput = input('Want to add another class? y/n: ')
            max_instances = input('What is the maximum number of training instances?: ')
            while 1:
                userclass_definedby = input('How do you want to define your class? (order,family,genus,genus_sex): ')
                if userclass_definedby == 'order':
                    class_definition = input('What order are you looking for? (Latin): ')
                    break
                if userclass_definedby == 'family':
                    class_definition = input('What family are you looking for? (Latin): ')
                    break
                if userclass_definedby == 'genus':
                    class_definition = input('What order are you looking for? (Latin): ')
                    break
                if userclass_definedby == 'genus_sex':
                    print('Sorry, Genus_Sex Functionality not yet ready...')
            print('Looking for dem photos')
            classfilter_index = Filter(zipfile, max_instances, userclass_definedby, class_definition,input_month,input_deployment_length, 0,0)
            user_class_name = input('What is the name of this class?: ')
            print(classfilter_index)
            print(len(classfilter_index))
            #dtype1 = np.dtype([('gender', '|S1'), ('height', 'f8')])
            a = np.loadtxt(media_links, dtype = str, skiprows=1, usecols=(3))
            a = np.extract(classfilter_index,a)
            #x = np.arange(len(a), dtype=int)
            print(len(a))
            b = np.full(len(a),user_class_name,dtype=('U', 10))
            print(len(b))
            class_array = np.stack((b,a), axis=-1)
            print(class_array)
            export_array = np.append(export_array,class_array)
            print(export_array)
            break
        if input_anotherclass == 'n':
            break
        else:
            print('Incorrect Key Selected, please choose y or n...')

    print('Successful - Let\'s make this AI algorithm!!')


zipfile = 'test_GBIF_Scrape.zip'#'/home/cxl_garage/Desktop/CXL_GBIF_Scrape.zip'
media_links = 'test_GBIF_Scrape/multimedia.txt'#'/home/cxl_garage/Desktop/CXL_GBIF_Scrape/multimedia.txt'
#userinput()


#print(Filter_pandas())

exampleLoop('pandas')
