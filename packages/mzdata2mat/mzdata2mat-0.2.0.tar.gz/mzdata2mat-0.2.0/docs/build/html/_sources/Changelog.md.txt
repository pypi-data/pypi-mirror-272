
# Changelog

## Version `0.2.0`
### Key elements of this release
### New features
- New module `classes` where all classes are stored.<br>
Logs are now printed in color within the console. Yellow for warnings, red for errors, and blue for information.

#### New class `matStruct`
- Use this class to personnalize the way the data is saved into `.mat` files. For example, if you want to save the mz values with a custom variable, you can set the new variable's name with :
```python 
matStruct.mz = "newName"
```
- All exported variable's names can now be modified with this class. <u>Note :</u> This does not modify the variable's names inside the `mzData` class, those names will remain the same. This change only applies to exported matlab files. Available properties :
    - fileName
    - filePath
    - metadata
    - mz
    - intensities
    - time
- When you call `saveMatfile` function, specify this class in the function, and the matlab file will be generated according to the names set inside this class.<br>
This class could also be used while loading matlab files with the new `loadMatfile` function. See below for further details.

#### mzDataManager
- New method `loadMatfile` which can loads created mat files and convert them into `mzData` class if their structure is compatible.
- Extended classe's functionnalities to handle personnalized mat files with `matStruct` class.

#### mzData
- New methods `setAttribute`, `getAttribute`, `getAttributesNames`, `clearAttributes` and `deleteAttribute`. Those mathods gives now the possibility to the user to add new fields inside the `mat` file created. All attributes created will be available inside the variable `extra` in Matlab.
- New method `fromDict`, whichs parses a dictionnary into a `mzData` class. Compatible data types : `str` and `dict`.
- Added parameter `oneStruct` to `toDict` function to specify if the data should be saved into one variable or exploded into multiple ones (i.e weather group data in a matlab structure or not).
- Extended classe's functionnalities to handle files with custom structure with `matFile` class.

### Bug fixes
- Fixed a bug when setting `customDirectory` to `True` was preventing `mzDataManager` class from initializing.
- Fixed a bug preventing saving the `.mat` file while using `customDirectory`
- Fixed a bug preventing exported files being named properly.
- Fixed a bug with `mzDataXMLread`. When `mzDataManager` class was initialized without path, the variable inside the `mzData` class `filePath` was not correct.

### List of possible error codes
- 3  - Invalid Directory
- 4  - No save directory specified
- 10 - Invalid mzData Directory
- 11 - Incompatible type
- 13 - Can't delete a system attribute
- 14 - Invalid Attribute
- 15 - Invalid dictionnary
- 19 - Invalid data Type
- 20 - mzData structure Incomplete

### Other
- Added test files to GitHub repository.
- Updated package's tags in PyPI.
- Removed duplicated Changelog file.
- Improved documentation

### Release date : 05/07/2024

## Version `0.1.0` and `0.1.1`
### Key elements of this release
- Removed usage of deprecated packages (PyExecJS)
- Added new dependant package (JSPyBridge)
- __Added Windows 11 compatibility__
- __Extended compatibility__ to python versions between `3.9` and `3.12` !
- Added metadata to the mat file created. Contents :
    - software
    - analyser
    - detector
- Added function `convertFile` which converts directly the mzData file into matlab file without calling `mzDataXMLread` and `saveMatfile` separatly.
- Created the `errors` module which contains the possible exceptions.
- Added debug elements to the CLI (`mzdata2mat-verify`) which prints into the console the verify status.
- Reduced package's size
- __Opened a GitHub__ for the package. If you encounter any bug, open an issue there.
- __New documentation__ available on [mzdata2mat.readthedocs.io](https://mzdata2mat.readthedocs.io). Go check it out !
- Added this changelog to keep track of the new realeases and changes.
- Various improvements & bug fixes

### Release date : 03/27/2024

## Version `0.0.1` to `0.0.22`
### Key elements of those releases
- First release of the software
- macOS only compatible
- Python version required : `3.12`
- CLI for verifying successful intallation : `mzdata2mat-verify`
- Bug fixes and improvements

### Release date : 03/21/2024
