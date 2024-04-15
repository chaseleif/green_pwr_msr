#! /usr/bin/env python3

import cpuinfo, os, psutil, threading

def getmachinespec(csvname='cpuinfo', new=False):
  if not new and os.path.isfile(csvname):
    machine = {}
    cast = lambda key, val: int(val) if key!='frequency' else float(val)
    with open(csvname,'r') as infile:
      for line in infile.readlines():
        parts = line.rstrip().split()
        machine[parts[0]] = cast(parts[0], parts[1])
  else:
    machine = cpuinfo.get_cpu_info()['brand_raw']
    machine = { 'number_of_cores':os.cpu_count(),
                'number_of_threads':os.cpu_count()*threading.active_count(),
                'frequency':psutil.cpu_freq()[2]/1000,
                'processor_manufacturer':0 if 'AMD' in machine \
                                    else 1 if 'Intel' in machine \
                                    else 2,
                'processor':18 }
    with open(csvname,'w') as outfile:
      for key, val in machine.items():
        outfile.write(f'{key} {val}\n')
  return machine

