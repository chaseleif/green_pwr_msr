#! /usr/bin/env python3

import numpy as np
import pandas as pd
import os, pickle, platform, psutil
from sklearn.preprocessing import PolynomialFeatures
from subprocess import Popen, PIPE
from time import time, sleep

class PowerModel:
  def __init__(self, machine):
    self.machine = machine
    self.polyfeat = PolynomialFeatures(degree=3, include_bias=False)

  def load(self, treepath, dfpath, modelpath):
    with open(treepath,'rb') as infile:
      self.tree = pickle.load(infile)
    self.df = pd.read_csv(dfpath)
    self.ytree = self.df[['id']]
    columns = [ 'number_of_cores','number_of_threads','frequency',
                'processor_manufacturer','processor' ]
    data = [self.machine[key] for key in columns]
    my_input_instance = self.tree.predict(pd.DataFrame([data],
                                                      columns=columns))
    i, c = np.where(self.ytree == my_input_instance)
    take_one_value = i[1]
    df = pd.read_csv(dfpath)
    columns = columns[-2:]+columns[:-2]+['load_percentile']
    self.input = df.loc[take_one_value,][columns]
    self.coredivisor = self.input[['number_of_cores']].iloc[0]
    with open(modelpath,'rb') as infile:
      self.powermodel = pickle.load(infile)

  def runcmd(self, output, cmd):
    csv = ['timestamp,power']
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    start = time()
    while True:
      self.input['load_percentile'] = psutil.cpu_percent(.1)
      poly = self.polyfeat.fit_transform(np.asarray(self.input).reshape(1,-1))
      power = self.powermodel.predict(poly)/self.coredivisor
      csv.append(f'{time()-start},{power.item()}')
      if proc.poll() is not None: break
    with open(output,'w') as outfile:
      outfile.write('\n'.join(csv)+'\n')

