from mzdata2mat import matStruct, mzDataManager
import os, sys

PATH = sys.argv[0].rsplit("/", maxsplit=1)[0]

struct = matStruct()
testFile = "tiny1.mzData.xml"
matFile = "tiny1.mat"

# Basic setup with directory
print("Test 1 started - Basic setup")
manager1 = mzDataManager(mzDataPath=PATH, exportPath=PATH, matStructure=struct)
manager1.convertFile(testFile, force=True, remove=False)
data1 = manager1.loadMatfile(matFile)
os.remove(os.path.join(PATH, matFile))
print("Test 1 finished")

# Setup without directory
print("Test 2 started - Without directory")
manager2 = mzDataManager(useDirectory=False, matStructure=struct)
manager2.convertFile(os.path.join(PATH, testFile), dir2Save=PATH, force=True, remove=False)
data2 = manager2.loadMatfile(os.path.join(PATH, matFile))
os.remove(os.path.join(PATH, matFile))

if data1 == data2:
    print("Both correct - Success")
else:
    print("Data different")

# With custom saving structure
modifiedStructure = matStruct()
modifiedStructure.metadata = "mData"
modifiedStructure.mz = "MZ"

print("Started testing for custom structure. With PATH")
manager1.matStructure = modifiedStructure
manager1.saveMatfile(data1)
data3 = manager1.loadMatfile(matFile)
if data3 == data1:
    print("Success with path")
os.remove(os.path.join(PATH, matFile))

manager2.matStructure = modifiedStructure
manager2.saveMatfile(data2, dir2Save=PATH)
data4 = manager2.loadMatfile(os.path.join(PATH, matFile))
if data4 == data2:
    print("Success without path")
os.remove(os.path.join(PATH, matFile))