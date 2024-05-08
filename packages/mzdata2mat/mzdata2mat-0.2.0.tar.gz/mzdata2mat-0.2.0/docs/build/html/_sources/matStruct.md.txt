# matStruct
## Presentation
The `matStruct` class is a class used to define correspondances between `mzData` variable names and desired names in Matlab.

## Definition
```python
class matStruct(BaseModel):
    metadata : str = None
    fileName : str = None
    filePath : str = None
    mz : str = None
    time : str = None
    intensities : str = None
    oneStruct : bool = True
```
## How to use
If you want to use default names, you can just omit the parameter inside the functions. Or you can define a variable holding default value with the following code :
```python
matlabStructure = matStruct()
```
By default variable content is equal to variable's name. So, for example, the string value of `matlabStructure.time` will be equal to `"time"`.<br>
Variable's are editable, so you can edit them if you want to change their values. For example, if you want to define `mz` to be `m/z`inside the matlab structure the following code is used : `matlabStruct.mz = "m/z"`.

If you want to save the data in one Matlab Structure (meaning that all variables will be group into one variable with the file's name), set `oneStruct` parameter to `True`, otherwise, set it to `False` and all variables will be saved in separated variables.

## Functions
### default
#### Presentation
This function resets the structure to it's default values. It gets called, whenever a new instance of this class is created, inside the class' initialization process.
#### Definition
```python
def default(self@matStruct)
```
#### How to use
```python
matlabStructure.default()
```
<u>Parameters</u>
- No parameters

<u>Outputs</u>
- No output, modify directly the class' values.

## Example

Let's consider a file exported as `sample.mat`. Inside are (if `oneStruct` is `True`):
- sample (name of file without `.mat`)
    - `fileName` : From which file this data was extracted
    - `filePath` : Where was located the file
    - `metadata`
        - software
        - analyser
        - detector
    - `mz`
    - `intensities`
    - `time`
---
If `oneStruct == False`, no containing structure is created, so data is exploded :
- `fileName` : From which file this data was extracted
- `filePath` : Where was located the file
- `metadata`
    - software
    - analyser
    - detector
- `mz`
- `intensities`
- `time`

## Notes
When the data is saved, a check will be done to see if all variables inside the `mzData` class were filled. If one or more variables are unset, the function will throw an error. In case you want to save incomplete data, specify the parameter `incompleteSave` in the save function. More info in [mzData class](mzData.md)