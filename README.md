# Green Code Power Measurement

Made from source taken from the VSCode plugin at this [link](https://marketplace.visualstudio.com/items?itemName=hzm7.greencode-powermeasurement).

"This extension is designed and developed for measuring power consumption of a code regardless of platform specifications."

***Now freed from VSCode!***
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
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install numpy pandas psutil py-cpuinfo scikit-learn
```
___
## Basics
`driver.py` is a simple driver, it drives 3 main tasks:
1) Gather and record CPU info
2) Initialize the powermodel
3) Tell the powermodel to execute the command
___
## Usage
To test usage, run the driver without arguments and `sleep 7` will be used as the command.
```bash
$ python3 driver.py
```

Or, run any other command.[^1]
```bash
$ python3 driver.py ../../mybigapp arg1 arg2
```

Optionally, a directory can be specified which will the command will be executed from:
```bash
$ python3 driver.py --directory=../../ mybigapp arg1 arg2
```

The final arguments of driver.py should be the command and arguments that will be sent to POpen.[^1]

[^1]: For more information on how the process is launched: [POpen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)
___

