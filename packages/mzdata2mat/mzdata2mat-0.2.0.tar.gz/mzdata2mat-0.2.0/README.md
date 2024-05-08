# mzdata2mat
Welcome ! `mzdata2mat` is a Python package from [LARTIC research team](https://lartic.fsaa.ulaval.ca/), which converts mzData.xml files (version 1.05, Agilent Technologies) into mat files readable using matlab. <br><br>
Author : Maxime R.A. Cordella<br>
Team leader : Pr. Christophe B.Y. Cordella<br><br>
Copyright(c)2024_LARTIC

[![Documentation Status](https://readthedocs.org/projects/mzdata2mat/badge/?version=latest)](https://mzdata2mat.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/mzdata2mat)](https://pypi.org/project/mzdata2mat/)
[![downloads](https://static.pepy.tech/badge/mzdata2mat/month)](https://pepy.tech/project/mzdata2mat)

## Documentation
The complete documentation is available [here](https://mzdata2mat.readthedocs.io/). All classes and methods are explained.

## Changelog
The current version of mzdata2mat is the following : `0.2.0`

You can see the complete changelog [here](https://github.com/MaximeLeMagicien/mzdata2mat/blob/main/Changelog.md)

## Compatible hardware
At this time, the following OSes have been tested :

### macOS
At this time, `macOS Sonoma 14.0` is officially supported, other macOS versions could be supported as long as they follow the requirements listed below.

### Windows
At this time, `mzdata2mat` have been tested and is supported on `Windows 11`, no testing has been done on Windows 10 or 7 but if you want to extend the compatibility, we are open to tester's feedback on thoses machines.

## Requirements
### Other than Python
This package __requires node.js installed__. you can download and install it at [nodejs.org](https://nodejs.org/en). It is available for both macOS and Windows for free.

### Python version
This package is compatible to any python version equal or newer than `3.9`.

### Python packages
When mzdata2mat will be installed on your system, the following packages will also be installed (if they are not) into your Python enviuronment : 
```
    pydantic>=2.6.4
    mat4py>=0.6.0
    javascript>=1!1.1.3
    colorama>=0.4.6
```
# Installation
From your terminal run the following command to install mzdata2mat into your environment :
```shell
$ pip install mzdata2mat
```
If you have multiple instances of Python installed, run this command with the chosen Python interpreter to install mzdata2mat in the corresponding Python installation :
```shell
$ <pathToPythonApp> -m pip install mzdata2mat
```
When the command terminates, you have successfully installed mzdata2mat !

To verfiy if the installation was successful, run in your terminal this command :
```shell
$ mzdata2mat-verify
```
When you will first run this command, node.js will download and install the `mzdata` package from `npm`. This will only happen the first time you run the command. The terminal will show you these lines during the process :
```shell
 Installing 'mzdata' version 'latest'... This will only happen once. 

added 7 packages, and audited 8 packages in 2s

1 package is looking for funding
  run `npm fund` for details

found 0 vulnerabilities

 OK. 
[JSE] 

[JSE] 
```
When it's done, mzdata2mat package will attempt to convert an example .mzdata.xml file into a .mat file. If everything goes right, you will get this message :
```shell
$ mzdata2mat - Ready to use !
```
The example file (.mzdata.xml) will be copied in the current working directory and the converted file (.mat) will be added as soon as the conversion finishes.

If an error occurs, this probably means that you do not have __node.js__ installed on your machine or you didn't add it to your PATH.

# Usage

### Example Code

```python

# Here we import the main class used for the conversion.
1 from mzdata2mat import mzDataManager

# We initialize the class
# If all mzData files are stored in the same directory, we can specify the parameter `mzDataPath` instead of `useDirectory`.
2 converterAgent = mzDataManager(useDirectory=False)

3 path2mzDataFile : str = "path/to/stored/files"

4 someDirectory : str = "path/to/save/file/"

# Now we can call the mzDataXMLread function to read the .mzData.xml file:
5 data = converterAgent.mzDataXMLread(fileName=path2mzDataFile)

# The data we've got from the previous function can be saved to a .mat file with the saveMatfile funtion:
6 converterAgent.saveMatfile(mzData=data, dir2save=someDirectory)

```

You have successfully converted a mzData file into mat files ! 

Congratulations !
