# Green Code Power Measurement

Derived from source taken from the VSCode plugin at this [link](https://marketplace.visualstudio.com/items?itemName=hzm7.greencode-powermeasurement).

"This extension is designed and developed for measuring power consumption of a code regardless of platform specifications."

Reused the plugin's data files and duplicated its functionality in Python3.
___
## Requirements
Python packages:
- numpy
- pandas
- psutil
- py-cpuinfo
- scikit-learn
___
### Setup requirements with PIP
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install numpy pandas psutil py-cpuinfo scikit-learn
```
___
## Basics
`driver.py` is a simple driver, it performs 3 main tasks:
1) Gathers and records CPU info
2) Initializes the powermodel
3) Sends the command to the powermodel
___
## Usage
To test usage, run `driver.py` without arguments and `sleep 7` will be called as the command.

To run some other command:
`python3 driver.py ../../mybigapp arg1 arg2`

- For more information on how the process is launched: [POpen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)
___
