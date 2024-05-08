class mzDataError(Exception):
    """Class used by mzdata2mat package to throw errors"""

    def __init__(self, errorMsg : str, errorCode : int):
        """Class used by mzdata2mat package to throw errors"""
        self.errorMsg = errorMsg
        self.errorCode = errorCode
        super().__init__(f"An error occured : Error {self.errorCode} - {self.errorMsg}")