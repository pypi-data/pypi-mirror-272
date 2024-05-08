# mzData

## Presentation
This is the Base class which holds all the data collected from a given `mzdata.xml` file. This is the data class used when the `mzDataManager` creates a `.mat` file.<br>
You can create your own instances of this class if your data is not collected from the mzData files.

## Definition
```python
class mzData(BaseModel):
    fileName : str = None
    filePath : str = None
    metadata : dict = None
    mz : list[list[float]] = [[]]
    intensities : list[list[float]] = [[]]
    time : list[float] = []
    oneStruct : bool = True
```

## How to use
There are two ways of creating this class, the first one is the following :
```python
# Class creation
data = mzData()

# The script below could be called anywhere you want, just be sure to fill all necessary data before calling the saveMatfile function from the mzdataManager class.
data.fileName = "sample.mzdata.xml"
data.filePath = "some/path/"
data.metadata = {
    'software' : 'someSoftware',
    'analyser' : 'John Doe',
    'detector' : 'someDetector'
}
data.mz = mzList
data.intensities = intensitiesList
data.time = timeList
data.oneStruct = True
```
If you have all informations at the same time, you could use the second way of defining the class :
```python
data = mzData(
    fileName = "sample.mzdata.xml",
    filePath = "some/path/",
    metadata = {
    'software' : 'someSoftware',
    'analyser' : 'John Doe',
    'detector' : 'someDetector'
    },
    mz = mzList,
    intensities = intensitiesList,
    time = timeList
)
```

## Functions

### fromDict
#### Presentation
Use `fromDict` function to populate the current `mzData` class based on a given `dict`.

#### Definition
```python
def fromDict(self@mzData, toParse : Any, mat : matStruct = matStruct())
```

#### How to use
To use this function, you need to specify how the dictionnary is built with the parameter `mat` which is of type `matStruct` class (The dictionnary could contain more elements, but only elements listed in the parameter will be parsed). The second parameter is the data to parse `toParse`.

```{warning}
This data must always be a dictionnary. Meaning that the `toParse` parameter must be either of type `dict` or it's equivalent in `str`. Anything other than this will raise an error.
```
Call this function like this:
```python
data.fromDict(mat=someMatStructure, toParse=dictionnaryRepresentationOfData)
```
If the structure is the default one, you can omit the `mat` parameter.

### toDict
#### Presentation
Use this function to convert `mzData` structure into a dictionnary representation of the data. This function is automatically called inside the `saveMatfile` function in the `mzDataManager` class.

#### Definition
```python
def toDict(self@mzData, mat : matStruct, partialSave : bool = False) -> dict
```

#### How to use
This function takes two input parameters. The first one, `mat` is a `matStruct` class which specifies how the dictionnary should be generated. See [matStruct class](matStruct.md) for further details.<br>
The second input parameter is a boolean `partialSave`. Set this parameter to `True` if you want to save a partial structure (i.e an incomplete `mzData` structure where, for example, time values are not specified. This parameter is by default set to `False`). If an incomplete structure is found and `partialSave` is not `True`, an error of class `mzDataError` will be raised.

With an already created `mzData` object, call the function like follows :
```python
convertedDict = data.toDict(mat=someMatStruct, partialSave=False)
```
The dictionnary generated will be containing the content inside the `data` variable.

### setAttribute
#### Presentation
This function gives the possibility to the user to define new properties or modify existing one inside the `extra` field of the class.
#### Definition
```python
def setAttribute(self@mzData, attributeName : str, attributeValue : Any)
```
#### How to use
The `setAttribue` function expects two input variables. The first one `attributeName` is a `str` and will be the new property's name. The second one called `attributeValue` corresponds to it's given value. This value could be a string, an integer or a dictionnary.
```{admonition} Info
Sets are not allowed at this time.
```

For example, let's say you want to create a new attribute called `uniqueIdentifier` which will be equal to an integer. To define such attribute, use the following code :
```python
# Considering that the data variable is an instance of the mzData class initialized with the default values.

data.setAttribute(attributeName="uniqueIdentifier", attributeValue=2846)
```
It is not possible yet to define an empty attribute with no value associated with it. This is a feature which will be added in a future release. 
```{warning}
Whenever you create a new attribute, you need to give it a value even if it is a blank string.
```

### getAttribute
#### Presentation
This one is pretty straight forward, returns the current value associated with the given attribute name.

#### Definition
```python
def getAttribute(self@mzData, attributeName : str)
```

#### How to use
This function takes one parameter `attributeName` as a `str`. Here is how to get the associated value of the attribute `uniqueIdentifier` defined above :

```python

ID = data.getAttribute(attributeName="uniqueIdentifier")
# ID should be equal to 2846

```
If the attribute doesn't exists, an error will be thrown by this function with the type `mzDataError`.

### getAttributeNames
#### Presentation
This function returns all defined attributes names as a list of string values.

#### Definition
```python
def getAttributesNames(self@mzData)
```

#### How to use
The usage of `getAttributeNames` function is pretty straight forward. From an already created `mzData` object call the function as shown below :
```python
# Considering data a variable of `mzData` class

attributes = data.getAttributesNames()

# With previously defined attributes in this page, this function should results :
# attributes = ["uniqueIdentifier"]
```

### deleteAttribute
#### Presentation
`deleteAttribute` function removes the given attribute name as a `str` from the list of custom attributes. Throws an error if the attribute name is not found.

#### Definition
```python
def deleteAttribute(self@mzData, attributeName : str)
```

#### How to use
From an already initialized `mzData` class, use the following code to call this function :
```python
data.deleteAttribute(attributeName="uniqueIdentifier")
```
This function is a void, so it doesn't returns any value. If an error occurs, it will be thrown.

### clearAttributes
#### Presentation
This function removes all custom user defined attributes. Use this function carefully because it removes everything. Use `removeAttribute` to have a better control over the available attributes.

#### Definition
```python
def clearAttributes(self@mzData)
```

#### How to use
```python
data.clearAttributes()
```
There is no return to this function.