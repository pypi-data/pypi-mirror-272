import yaml
from .Scheme import Scheme
from .DataMill import DataMill

class DataBlob:
    def __init__(self, configFile, dataRoot, dataMill=None):
        with open(configFile, 'r') as file:
            config = yaml.safe_load(file)
        if isinstance(config, dict):
            self.schemeKeys = list(config.keys())
            self.schemes = {}
        else:
            raise TypeError('Import Error')

        #self.verifyConfigStructure()
        self.loadSchemes(config)

        if dataMill is None:
            self.dataMill = DataMill(dataRoot, self.schemes)
        self.data = self.dataMill.mainDataFrame


    def loadSchemes(self, configData):
        for key in self.schemeKeys:
            self.schemes.update({key : Scheme(key, configData)})

    def verifyConfigStructure(self):
        numberOfMains = 0
        for scheme in self.schemes:
            if (scheme.main):
                numberOfMains +=1
        if(numberOfMains > 1):
            raise ValueError('Too many main datapoints')