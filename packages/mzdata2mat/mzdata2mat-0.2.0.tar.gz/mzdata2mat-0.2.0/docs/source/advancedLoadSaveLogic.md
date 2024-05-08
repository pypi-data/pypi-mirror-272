# Advanced load and save logic

## Presentation
In this section the advanced load and save structure will be explained and examples will be given to illustrate the documentation.

```{warning}
This is an advanced topic, if you are not familiar with the package, we highly recommand to check the [basic code example](code-example.md) first.
```

## Example 1 : Load custom structure

### From a matlab file
In this example, we are going to load a custom matlab structure containing m/z values into a mzData class. Let's get started !

Here is the matlab file's content :<br>
`sampleTest.mat`
- sampleTest
    - echName
    - mData
    - path
    - times
    - m/z
    - intensities

To be able to load this data properly, let's define a `matStruct` class where we specify which field is which :
```python
from mzdata2mat.classes import matStruct

savedDataStruct = matStruct(
    oneStruct = True,
    metadata = "mData",
    fileName = "echName",
    filePath = "path",
    mz = "m/z",
    time = "times"
)
```
```{tip}
Since the variable `intensities` is the same in the class as inside the matlab structure, we can omit it's declaration.
```

Now that's our matlab structure is defined, let's load the data into a variable :
```python
from mzdata2mat import mzDataManager

manager = mzDataManager(matStructure=savedDataStruct)
sampleTestData = manager.loadMatfile(fileName="sampleTest.mat")

```
Our data is now stored inside the `sampleTestData` variable. We can now access the data by referencing the varaible. For example, let's say I want to get the file's name. In the file the variable was `echName`, we now know that this variable corresponds with the `fileName` property. So, we get the value like this : `sampleTestData.fileName`. 

```{admonition} Teaser !
In the future, features will be added to expose those properties directly inside the variable insdead of a generic name. For instance, `echName` will be directly accessible by the following code `sampleTestData.echName`. More information about this feature in the future.
```

### From a dictionnary
To load a `mzData` structure from a dictionnary representation, the process is almost the same.<br>
Here is how to achieve this :
```python
# Instead of calling the loadMatfile function from the mzDataManager class,
# we need to directly create an instance of the `mzData` class.

from mzdata2mat import mzData

dictData = mzData()
dictData.fromDict(
    toParse=someDictionnary,
    mat=matRepresentation
)
# We don't need to instantiate the mzDataManager class for this parse.
# But you will need an instance in order to save the data to a Matlab file.
```

```{warning}
`toParse` should be of type `str` or `dict` only. If your data is formated in the default reprentation, you can omit the `mat` parameter.
```

## Example 2 : Save custom structure
In this example, we are going to save an already existing `mzData` variable into a matlab file with custom fields. Let's get started !<br>
The process is really easy and much shorter than the one for loading custom data.

The same logic applies for defining the `matStruct` variable (see above for how to define the matlab structure you want to have).

This code saves the `sampleTestData` variable according to the corresponding `matStruct` defined in the custom loading logic.

```python
manager.saveMatfile(mzData=sampleTestData):
```

```{tip}
The custom save structure doesn't need to be passed while calling this function. The manager saves the data according to the structure given in it's initalization. To modify it add this line before : `manager.matStruct = someNewStructure`.
```

This function has a lot of parameters. To have a complete description of its functionnalities check [this page](mzDataManager.md#savematfile).