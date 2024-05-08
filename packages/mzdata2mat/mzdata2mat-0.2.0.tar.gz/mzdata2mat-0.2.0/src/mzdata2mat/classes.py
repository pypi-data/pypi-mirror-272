from typing import Any
from pydantic import BaseModel
import datetime
from .errors import mzDataError
import json
from datetime import datetime

class mzDataXMLStruct(BaseModel):
    metadata : dict
    times : list[float]
    series : Any

class matStruct(BaseModel):
    """
        Creates an instance of `matStruct` class. Used to associate variable names between files.
    """
    metadata : str = None
    fileName : str = None
    filePath : str = None
    mz : str = None
    time : str = None
    intensities : str = None
    oneStruct : bool = True

    def __init__(self):
        """
        Creates an instance of `matStruct` class. Used to associate variable names between files.
        """
        super().__init__()
        self.default()

    def default(self):
        """
        Resets class' variables names to the default values.
        """
        self.metadata = "metadata"
        self.fileName = "fileName"
        self.filePath = "filePath"
        self.mz = "mz"
        self.intensities = "intensities"
        self.time = "time"
        self.oneStruct = True

class mzData(BaseModel):
    """
        Class used to handle all conversions and tranfers between `.mzData.xml` files, matlab files and Python.
    """
    fileName : str = ""
    filePath : str = ""
    metadata : dict = {}
    mz : list[list[float]] = [[]]
    intensities : list[list[float]] = [[]]
    time : list[float] = []
    __extra__ : dict = {}

    def __init__(self):
        """
        Class used to handle all conversions and tranfers between `.mzData.xml` files, matlab files and Python.
        """
        super().__init__()
        self.__extra__['createdDate'] = f"{datetime.now()}"
        self.__extra__['lastModifiedDate'] = self.__extra__['createdDate']

    def setAttribute(self, attributeName : str, attributeValue : Any):
        """
        Creates a new attribute with name `attributeName` and value `attributeValue`.\n
        If the attribute already exists, updates the current value.
        """
        self.__extra__[attributeName] = attributeValue
        return
    
    def getAttribute(self, attributeName : str):
        """
        Gets the value of `attributeName`. If attribute doesn't exists, raises an error of type `mzDataError`.
        """
        try:
            list(self.__extra__.keys()).index(attributeName)
            return self.__extra__[attributeName]
        except ValueError:
            raise mzDataError(f"Invalid Attribute, attribute {attributeName} does not exists", 14)

    def getAttributesNames(self) -> list:
        """
        Returns all user defined attribute names.
        """
        names = list(self.__extra__.keys())
        names.pop(names.index('createdDate'))
        names.pop(names.index('lastModifiedDate'))
        return names

    def deleteAttribute(self, attributeName : str):
        """
        Deletes specified user defined attribute.
        """
        try:
            if attributeName != ('createdDate' or 'lastModifiedDate'):
                list(self.__extra__.keys()).index(attributeName)
                self.__extra__.pop(attributeName)
                return
            else:
                raise mzDataError("The attribute specified is a system attribute, it can't be deleted.", 13)
        except ValueError:
            raise mzDataError(f"Invalid Attribute, attribute {attributeName} does not exists", 14)

    def clearAttributes(self):
        """
        Clears all user defined attributes.
        """
        cDate = self.__extra__['createdDate']
        mDate = self.__extra__['modifiedDate']
        self.__extra__ = {}
        self.__extra__['createdDate'] = cDate
        self.__extra__['modifiedDate'] = mDate
        return

    def fromDict(self, toParse : Any, mat : matStruct = matStruct()):
        """
        Parses a dictionnary representation of mzData structure from `toParse` parameter and the provided Matlab structure in `mat` parameter.\n
        `toParse` should be of type `str` or `dict`.
        """
        dump = mat.model_dump(exclude=['oneStruct'])
        keys = list(dump.keys())
        if type(toParse) == str:
            try:
                JSON : dict = json.loads(toParse)
                content = JSON[list(JSON.keys())[0]]
                if mat.oneStruct:
                    for key in keys:
                        self.__setattr__(key, content[dump[key]])
                else:
                    for key in keys:
                        self.__setattr__(key, JSON[dump[key]])
                return
            except json.JSONDecodeError as e:
                raise mzDataError(f'Invalid dict , got following error while parsing : {e.msg}', 15)
        elif type(toParse) == dict:
            if mat.oneStruct:
                key = list(toParse.keys())
                content : dict = toParse[key[0]]
                for element in keys:
                    self.__setattr__(element, content[dump[element]])
                try:
                    list(content.keys()).index('extra')
                    self.__extra__ = content['extra']
                except ValueError:
                    pass
            else:
                for element in keys:
                    try :
                        self.__setattr__(element, toParse[dump[element]])
                    except KeyError:
                        pass
                try:
                    list(toParse.keys()).index('extra')
                    self.__extra__ = toParse['extra']
                except ValueError:
                    pass
            return
        else:
            raise mzDataError(f"Data provided is not of type dict or str, got {type(toParse)}", 19)
        
    def __checkFields__(self):
        notFilled : list = []
        if self.fileName == "":
            notFilled.append("fileName")
        if self.filePath == "":
            notFilled.append("filePath")
        if self.intensities == []:
            notFilled.append("intensities")
        if self.mz == []:
            notFilled.append("mz")
        if self.time == []:
            notFilled.append("time")
        if self.metadata == {}:
            notFilled.append("metadata")
        if len(notFilled) == 0:
            return True
        else:
            return notFilled

    def toDict(self, mat : matStruct = matStruct(), partialSave : bool = False) -> dict:
        """
        Creates a dictionnary representation of the data according to the parameters provided.
        """
        canSave = self.__checkFields__()
        if canSave == True or partialSave == True:
            copyright : dict = {
            'Author' : '(c)LARTIC_2024_Maxime_CORDELLA',
            'URL' : 'https://lartic.fsaa.ulaval.ca/chimiometrie/routines-de-conversion'
            }
            tempDict = self.model_dump()
            dump = mat.model_dump(exclude=['oneStruct'])
            keys = list(dump.keys())
            if type(canSave) == list:
                for element in canSave:
                    tempDict.pop(element)
                    keys.pop(keys.index(element))
            newDict : dict = {}
            for key in keys:
                newDict[dump[key]] = tempDict[key]
            newDict['copyright'] = copyright
            newDict['documentation'] = "https://mzdata2mat.readthedocs.io/"
            newDict['extra'] = self.__extra__
            date = datetime.now()
            try:
                newDict['extra']['createdDate']
            except KeyError:
                newDict['extra']['createdDate'] = f"{date}"
            newDict['extra']['modifiedDate'] = f"{date}"
            if mat.oneStruct:
                return {self.fileName.lower().split(".mzdata")[0] : newDict}
            else:
                return newDict
        else:
            raise mzDataError(f"mzData structure is incomplete, please fill all the fields. Following fields are not filled : {canSave}. Set incomplete save to True if you want to save partial structure.", 20)
