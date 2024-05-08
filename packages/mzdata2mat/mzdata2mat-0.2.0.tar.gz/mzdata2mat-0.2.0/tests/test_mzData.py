from mzdata2mat import mzData, matStruct


data1 = mzData()
data2 = mzData()

struct = matStruct()
struct.fileName = "Name"
struct.time = "times"
struct.oneStruct = False

customDict = {
    'Name' : 'something.mzdata.xml',
    'filePath' : 'some/path',
    'metadata' : {},
    'mz' : [],
    'intensities' : [],
    'times' : [],
    'extra' : {
        'createdDate' : 'now',
        'lastModifiedDate' : 'now'
    }
}

defaultDict = {
    'something' : {
        'fileName' : 'something.mzdata.xml',
        'filePath' : 'some/path',
        'metadata' : {},
        'mz' : [],
        'intensities' : [],
        'time' : [],
        'extra' : {
            'createdDate' : 'now',
            'lastModifiedDate' : 'now'
        }
    }
}

# Load from dictionnary and custom structure
data1.fromDict(customDict, struct)

data2.fromDict(defaultDict)

assert data1 == data2

data1.setAttribute("testAttribute", "simpleValue")
data1.setAttribute("intAttribute", 3)
data1.setAttribute("floatAttribute", 0.5)
data1.setAttribute("listAttribute", ["test", 1])

data2.setAttribute("testAttribute", "simpleValue")
data2.setAttribute("intAttribute", 3)
data2.setAttribute("floatAttribute", 0.5)
data2.setAttribute("listAttribute", ["test", 1])

assert data1.getAttributesNames() == data2.getAttributesNames()

# Default export
# Since we don't have any data we specify partialSave parameter to True
assert data1.toDict(partialSave=True) == data2.toDict(partialSave=True)

# Custom export
# Since we don't have any data we specify partialSave parameter to True
assert data1.toDict(struct, partialSave=True) == data2.toDict(struct, partialSave=True)