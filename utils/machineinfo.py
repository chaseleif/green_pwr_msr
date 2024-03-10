#! /usr/bin/env python3

import cpuinfo, os, psutil

def getmachinespec(csvname='cpuinfo', new=False):
  if not new and os.path.isfile(csvname):
    machine = {}
    cast = lambda key, val: int(val) if key!='frequency' else float(val)
    with open(csvname,'r') as infile:
      for line in infile.readlines():
        parts = line.rstrip().split()
        machine[parts[0]] = cast(parts[0], parts[1])
  else:
    # The multiplier, 2, for number_of_threads is copied from the original
    # os.cpu_count() returns logical cores already, unsure of the intent
    # The original misclassified my Intel(R) as other, since it != 'Intel'
    # processor was unconditionally set to -1 in the original
    machine = cpuinfo.get_cpu_info()['brand_raw'].split()
    machine = { 'number_of_cores':os.cpu_count(),
                'number_of_threads':os.cpu_count()*2,
                'frequency':psutil.cpu_freq()[2]/1000,
                'processor_manufacturer':0 if machine[0].startswith('AMD') \
                                    else 1 if machine[0].startswith('Intel') \
                                    else 2,
                'processor':-1 }
    with open(csvname,'w') as outfile:
      for key, val in machine.items():
        outfile.write(f'{key} {val}\n')
  return machine

