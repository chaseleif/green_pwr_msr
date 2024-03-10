#! /usr/bin/env python3

import argparse, os, sys
from models.powermodel import PowerModel
from utils.machineinfo import getmachinespec

if __name__ == '__main__':
  parser = argparse.ArgumentParser( add_help=False,
                                    description='This utility measures ' + \
                                      'power consumption of a program',
                                    argument_default=argparse.SUPPRESS,
                                    prog=sys.argv[0])
  parser.add_argument('-h', '--help', action='store_true',
                      help='Show this help message')
  #parser.add_argument('--model', metavar='<model>',
  #                    choices=['PowerModel'], default='PowerModel',
  #                    help='Specify the power model to use')
  parser.add_argument('-n', '--new', action='store_true', default=False,
                      help='Regenerate machine information file')
  parser.add_argument('-o', '--output', metavar='<output.csv>',
                      default='poweruse.csv',
                      help='Specify the power-use output filename')
  parser.add_argument('-d', '--dir', metavar='<directory>',
                      default=None,
                      help='Specify the directory to execute command from')
  parser.add_argument('command', nargs='*',
                      default=['sleep','7'],
                      help='Specify the command and arguments to execute')
  args = vars(parser.parse_args())
  if 'help' in args:
    parser.print_help()
    sys.exit(0)
  model = PowerModel(getmachinespec(os.path.join('data','cpuinfo'),
                                    new=args['new']))
  model.load( treepath=os.path.join('data','DecisionTree.pickle'),
              dfpath=os.path.join('data','my_df_up.csv'),
              modelpath=os.path.join('data','powermodel.pickle'))
  model.runcmd(output=args['output'],cmd_dir=args['dir'],cmd=args['command'])

