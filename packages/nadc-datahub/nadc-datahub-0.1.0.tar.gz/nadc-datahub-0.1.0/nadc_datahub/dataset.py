from typing import Dict
from dataclasses import dataclass
class DataSet:
    def auth(self, username="", password="", token=""):
        # code for authentication
        raise NotImplementedError()

    def download(self,output, datatype, metadatas: Dict):
        # code for downloading data
        raise NotImplementedError()

    def authorized(self):
        # code for checking authentication
        raise NotImplementedError()
    
    def get_datatypes(self):
        # code for getting datatypes
        raise NotImplementedError()
    
@dataclass
class DataType:
    name: str
    description: str
    metadatas: Dict

