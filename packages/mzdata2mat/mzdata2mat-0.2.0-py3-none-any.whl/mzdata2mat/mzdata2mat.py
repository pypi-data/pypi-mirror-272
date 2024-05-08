from pydantic import BaseModel
from mat4py import savemat, loadmat
from mat4py.loadmat import ParseError
from javascript import require
from javascript.errors import JavaScriptError
from .errors import mzDataError
import os
import shutil
from .classes import matStruct, mzData, mzDataXMLStruct
from colorama import Fore

class mzDataManager(BaseModel):
    """Main class for converting .mzData.xml files into .mat files for realeases of Matlab r2019b and newer.
        -> `useDirectory` : Set this parameter to `False` to not use directories and specify them when using the functions.
        -> `mzDataPath` : Path to the folder containing the .mzdata.xml files \n
        -> `exportPath` : Path to save the converted .mat files \n
    """
    mzDataPath : str = None
    exportPath : str = None
    __mzDataPackage__ : str = None
    matStructure : matStruct = matStruct()

    def __init__(self, useDirectory : bool = True, mzDataPath : str = None, exportPath : str = None, matStructure : matStruct = None):
        """Main class for converting .mzData.xml files into .mat files for realeases of Matlab r2019b and newer.
            -> `useDirectory` : Set this parameter to `False` to not use directories and specify them when using the functions.
            -> `mzDataPath` : Path to the folder containing the .mzdata.xml files \n
            -> `exportPath` : Path to save the converted .mat files \n
        """
        super().__init__()
        if useDirectory:
            if os.path.isdir(mzDataPath) and os.path.exists(mzDataPath):
                self.mzDataPath = mzDataPath
            else:
                raise mzDataError("The directory entered for .mzdata.xml files is not valid", 3)
            if os.path.isdir(exportPath) and os.path.exists(exportPath):
                self.exportPath = exportPath
            else:
                raise mzDataError("The directory entered for converted .mat files is not valid", 3)
        if matStructure != None:
            self.matStructure = matStructure
        try:
            self.__mzDataPackage__ = require('mzdata')
        except Exception as e:
            # This error will often be related with node.js not being installed on the target machine.
            raise e

    def mzDataXMLread(self, fileName : str, customDirectory : bool = False):
        """
        Reads mzML files and returns the given object.\n
        -> `fileName` :\n
            -> Should be the full path to the file and it's extension (.mzdata.xml) to convert if no value was given to `mzDataPath` when initializing the class.\n
            -> Otherwise, the file's relative path with it's extension (.mzdata.xml)\n
        -> `customDirectory` : Set this parameter to `True` if the `fileName` is in a different path than the one given in configuration.
        """
        try:
            if self.mzDataPath == None or customDirectory:
                    if os.path.exists(fileName):
                        result = self.__mzDataPackage__.parseMZ(open(fileName).read())
                    else:
                        raise mzDataError("The path given for the mzData file is not valid.", 10)
            else:
                if os.path.exists(os.path.join(self.mzDataPath, fileName)):
                    result = self.__mzDataPackage__.parseMZ(open(os.path.join(self.mzDataPath, fileName)).read())
                else:
                    raise mzDataError("The path given for the mzData file is not valid.", 10)
        except JavaScriptError as e:
            raise e
        metadata = {
            'software' : str(result.metadata["software"]),
            'analyser' : str(result.metadata["analyser"]),
            'detector' : str(result.metadata["detector"])
        }
        dataStruct = mzDataXMLStruct(metadata=metadata, times=list(result.times), series=result.series["ms"]["data"])
        returnStruct = mzData()
        totalMasseDataSet = []
        totalIntensityDataSet = []
        for i in dataStruct.series:
            massesDataSet = []
            intensityDataSet = []
            for y in range(len(list(i[0]))):
                massesDataSet.append(i[0][str(y)])
            for z in range(len(list(i[1]))):
                intensityDataSet.append(i[1][str(z)])
            totalMasseDataSet.append(massesDataSet)
            totalIntensityDataSet.append(intensityDataSet)
        returnStruct.mz = totalMasseDataSet
        returnStruct.intensities = totalIntensityDataSet
        returnStruct.time = dataStruct.times
        if customDirectory or self.mzDataPath == None:
            file = fileName.rsplit("/", 1)[0]
        else:
            file = self.mzDataPath
        returnStruct.filePath = file
        try:
            returnStruct.fileName = fileName.rsplit("/", 1)[1]
        except IndexError:
            if fileName.find("\\") != -1:
                returnStruct.fileName = fileName.rsplit("\\", 1)[1]
            else:
                returnStruct.fileName = fileName
        returnStruct.metadata = dataStruct.metadata
        return returnStruct
    
    def saveMatfile(self, mzData : mzData, remove : bool = False, dir2Save : str = None, force : bool = False, fileName : str = None, partialSave : bool = False):
        """
        Saves a `mzData` structure to a .mat file.\n
        -> `mzData`     : The structure got from `mzMLread` function.\n
        -> `remove`     : Should the original file be removed when it is saved as .mat file ?\n
        -> `dir2Save`   : Save directory to save the .mat file. If path was given in configuration, it is not needed. This parameter will be prioritised over the path given in configuration (if any).\n
        -> `force`      : If a file has the same name in the converted folder, should it be replaced ? (File will not be saved if sibling found in convert folder and this parameter set to `False`.)
        """
        if self.exportPath == None or dir2Save != None:
            if os.path.exists(dir2Save):
                saveDir = os.path.join(dir2Save, f"{mzData.fileName.lower().split('.mzdata')[0] if fileName == None else fileName.split('.mat')[0]}.mat")
            else:
                raise mzDataError("No save directory specified", 4)
        else:
            saveDir = os.path.join(self.exportPath, f"{mzData.fileName.lower().split('.mzdata')[0] if fileName == None else fileName.split('.mat')[0]}.mat")
        
        if os.path.exists(saveDir):
            if force:
                os.remove(saveDir)
                savemat(saveDir, mzData.toDict(self.matStructure, partialSave=partialSave))
            else:
                print(Fore.BLUE+ f"Info : File {mzData.fileName} skipped because same file exists in export folder and parameter `force` is not set to `True`" + Fore.RESET)
        else:
            savemat(saveDir, mzData.toDict(self.matStructure, partialSave=partialSave))
        if remove:
            os.remove(os.path.join(mzData.filePath, mzData.fileName))
        return
    
    def convertFile(self, fileName : str, customDirectory : bool = False, dir2Save : str = None, force : bool = False, remove : bool = False):
        """
        Reads mzData.xml file and saves it directly into the folder specified.\n
        -> `fileName` :\n
            -> Should be the full path to the file and it's extension (.mzdata.xml) to convert if no value was given to `mzDataPath` when initializing the class.\n
            -> Otherwise, the file's relative path with it's extension (.mzdata.xml)\n
        -> `customDirectory` : Set this parameter to `True` if the `fileName` is in a different path than the one given in configuration.
        -> `dir2Save`   : Save directory to save the .mat file. If path was given in configuration, it is not needed. This parameter will be prioritised over the path given in configuration (if any).\n
        -> `force`      : If a file has the same name in the converted folder, should it be replaced ? (File will not be saved if sibling found in convert folder and this parameter set to `False`.)
        -> `remove`     : Should the original file be removed when it is saved as .mat file ?\n

        """
        fileContent = self.mzDataXMLread(fileName=fileName, customDirectory=customDirectory)
        self.saveMatfile(mzData=fileContent, remove=remove, dir2Save=dir2Save, force=force)
        return
    
    def loadMatfile(self, fileName : str, fromOneStruct : bool = True) -> mzData:
        """
        Creates a `mzData` structure from a matlab file.\n
        -> `fileName` : Full path of the matlab file to load the data from.
        -> `fromOneStruct` : Is the data contained in one variable ? Set this paramteter to `True` if that's the case.
        """
        PATH = ""
        if os.path.isfile(fileName):
            PATH = fileName
        
        elif self.mzDataPath != None:
            PATH = os.path.join(self.mzDataPath, fileName)
        
        else:
            raise mzDataError("No such file or directory.", 3)

        try:
            tempClass = mzData()
            data = loadmat(PATH)
            dump = self.matStructure.model_dump()
            if fromOneStruct:
                name : str = list(data.keys())[0]
                content = data[name]
            else:
                content = data
            for key in list(dump.keys()):
                try:
                    tempClass.__setattr__(key, content[dump[key]])
                except KeyError:
                    if key != "oneStruct":
                        print(Fore.YELLOW + f"Warning : {Fore.BLUE} {dump[key]} {Fore.YELLOW} corresponding to {Fore.BLUE + key} {Fore.YELLOW} field has not been found in mat file : Using default value in created structure."+Fore.RESET)
            try:
                list(content.keys()).index('extra')
                if content['extra'] == '':
                    tempClass.__extra__ = {}
                else:
                    tempClass.__extra__ = content['extra']
            except ValueError:
                tempClass.__extra__ = {}
            return tempClass
        except ParseError:
            raise mzDataError("Error while reading, some data have incompatible type.", 11)

def verify():
    print(Fore.BLUE + "Starting verifying process..." + Fore.RESET)
    try:
        path = os.getcwd()
        testFile = os.path.join(__file__.lower().rsplit("mzdata", 1)[0], "tiny1.mzData.xml")
        print(Fore.BLUE + "Creating class... " + Fore.RESET)
        testClass = mzDataManager(useDirectory=False)
        print(Fore.BLUE + "Copying file in current directory..." + Fore.RESET)
        shutil.copyfile(testFile, os.path.join(path, "tiny1.mzData.xml"))
        print(Fore.BLUE + "Reading file..." + Fore.RESET)
        value = testClass.mzDataXMLread(os.path.join(path, "tiny1.mzData.xml"))
        print(Fore.BLUE + "Saving file..." + Fore.RESET)
        testClass.saveMatfile(value, dir2Save=path, force=True)
        print(Fore.BLUE + "mzdata2mat - Ready to use !" + Fore.RESET)
    except Exception as e:
        raise e