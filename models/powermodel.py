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
    # The column order matters for use in the models
    columns = [ 'number_of_cores','number_of_threads','frequency',
                'processor_manufacturer','processor' ]
    data = [self.machine[key] for key in columns]
    with open(treepath,'rb') as infile:
      tree = pickle.load(infile)
    my_input_instance = tree.predict(pd.DataFrame([data], columns=columns))
    df = pd.read_csv(dfpath)
    i, c = np.where(df[['id']] == my_input_instance)
    # Seems arbitrary to use the 2nd element
    take_one_value = i[1]
    # The column order is rearranged for the powermodel to keep us on our toes
    columns = columns[-2:]+columns[:-2]+['load_percentile']
    # Get our one row, order the columns as expected
    self.input = df.loc[take_one_value,][columns]
    self.coredivisor = self.input[['number_of_cores']].iloc[0]
    with open(modelpath,'rb') as infile:
      self.powermodel = pickle.load(infile)

  def runcmd(self, output, cmd):
    csv = ['timestamp,power']
    # *no security checks or validation of the command*
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    start = time()
    while True:
      # Set the cpu percentage
      self.input['load_percentile'] = psutil.cpu_percent(.1)
      # Get our polynomial
      poly = self.polyfeat.fit_transform(np.asarray(self.input).reshape(1,-1))
      # Predict
      power = self.powermodel.predict(poly)/self.coredivisor
      # Log
      csv.append(f'{time()-start},{power.item()}')
      # proc.poll() will return None if cmd is still running
      if proc.poll() is not None: break
    with open(output,'w') as outfile:
      outfile.write('\n'.join(csv)+'\n')

