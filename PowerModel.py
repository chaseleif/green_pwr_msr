import numpy as np
import pandas as pd
import psutil
import csv
import pickle
import os.path
import platform
from pathlib import Path
import pathlib
from datetime import datetime
from sklearn.preprocessing import PolynomialFeatures

poly_features = PolynomialFeatures(degree=3, include_bias=False)

dir_name = pathlib.Path(__file__).parent.resolve()
csv_name ='cpu_info.csv'
csv_path = os.path.join(dir_name, csv_name)


#mypath = Path(csv_path)
test = False
if (Path(csv_path).exists()):
    test = True

dir_name = pathlib.Path(__file__).parent.resolve()
pyfile_name ='cpu_info.py'
pyfile_path = os.path.join(dir_name, pyfile_name)

if (test == False):
    from subprocess import call
    if(platform.system() == 'linux'):
        call(["python3", pyfile_path])
    elif(platform.system() == 'Linux'):
        call(["python3", pyfile_path])
    else:
        call(["python", pyfile_path])
        #print(platform.system())
        
with open("cpu_info.csv", 'r') as file:
    cpu_info = csv.reader(file)
    cpu_info_elements = list(cpu_info)

if len(cpu_info_elements) >= 1:
    my_number_of_cores = (cpu_info_elements[0][0])

if len(cpu_info_elements) >= 2:
    my_manufacturer_name = cpu_info_elements[1][0]

if len(cpu_info_elements) >= 3:
    my_processor = cpu_info_elements[2][0]

if len(cpu_info_elements) >= 4:
    my_number_of_threads = (cpu_info_elements[3][0])

if len(cpu_info_elements) >= 4:
    my_frequency = (cpu_info_elements[4][0])

if(my_manufacturer_name == 'AMD'):
    my_manufacturer_name = 0
elif(my_manufacturer_name == 'Intel'):
    my_manufacturer_name = 1
else: my_manufacturer_name = 2

my_processor_df_tree_no_id = {'number_of_cores': my_number_of_cores,	'number_of_threads': my_number_of_threads, 'frequency': my_frequency, 'processor_manufacturer': my_manufacturer_name, 'processor': -1}
my_processor_df_tree_convert_to_df_no_id = pd.DataFrame([my_processor_df_tree_no_id])
print(my_processor_df_tree_convert_to_df_no_id)

dir_name = pathlib.Path(__file__).parent.resolve()
dffile_name ='my_df_up.csv'
dffile_path = os.path.join(dir_name, dffile_name)

df = pd.read_csv(dffile_path)
y_tree = df[['id']]

tree_model_name = "DecisionTree.pickle"
tree_model_path = pathlib.Path(__file__).parent.resolve()
tree = os.path.join(tree_model_path, tree_model_name)
if os.path.exists(tree):
    decisionTree = pickle.load(open(tree, "rb"))
    my_input_instance = decisionTree.predict(my_processor_df_tree_convert_to_df_no_id)
else:
    print("TREE NOT FOUND")

i, c = np.where(y_tree == my_input_instance)
take_one_value = i[1]
my_row = df.loc[take_one_value,]

timestamp = 0

dir_name = pathlib.Path(__file__).parent.resolve()
file_name = 'power_log1.csv'

current_time = datetime.now().strftime("%Y%m%d%H%M%S")
file_name_with_time = f'power_log1_{current_time}.csv'
file_path1 = os.path.join(dir_name, file_name_with_time)

dir_name = pathlib.Path(__file__).parent.resolve()
file_name ='power_log1.csv'
file_path = os.path.join(dir_name, file_name)

model_name = "powermodel.pickle"
model_path = pathlib.Path(__file__).parent.resolve()
powermodel = os.path.join(model_path, model_name)

with open(file_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['timestamp', 'power'])
    while(1):
        my_processor_input = my_row[['processor_manufacturer',	'processor',	'number_of_cores',	'number_of_threads', 'frequency',	'load_percentile']]
        my_cpu_load = psutil.cpu_percent(.1)
        
        my_core_fix = my_row[['number_of_cores']]
        my_core_fix = my_core_fix.ravel()

        my_processor_input['load_percentile'] = my_cpu_load
        my_processor_input = np.asarray(my_processor_input)
        my_processor_input = my_processor_input.reshape(1, -1)
        my_processor_input_poly = poly_features.fit_transform(my_processor_input)

        if os.path.exists(powermodel):
            model = pickle.load(open(powermodel, "rb"))
            my_power = model.predict(my_processor_input_poly)/my_core_fix
            writer.writerow([timestamp, my_power.item()])
            #print(my_processor_input)
            #print(my_power)
            timestamp = timestamp + 10
            output_file.flush()
        else:
            print("Model File Missing")