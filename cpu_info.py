import csv
import psutil
import cpuinfo
from os import cpu_count

my_cpu_info = cpuinfo.get_cpu_info()['brand_raw']
splited_cpu_info = my_cpu_info.split()
with open('cpu_info.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow([cpu_count()])
    writer.writerow({splited_cpu_info[0]})
    writer.writerow({splited_cpu_info[3]})
    writer.writerow([cpu_count()*2])
    writer.writerow(([(psutil.cpu_freq())[2]/1000]))