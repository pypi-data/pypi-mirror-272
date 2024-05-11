from .YaModules import *



class Scheme():

    def __init__(self, key, configFile):
        self.key = key

        self.main = False
        self.aliases = []
        self.label = ''
        self.mandatoryMetaData = []
        self.optionalMetaData = []
        self.filters = []
        self.classifiers = []

        self.unpack(configFile)

    def unpack(self, configFile):
        rawDict = configFile[self.key]
        self.getMain(rawDict)
        self.getAliases(rawDict)
        self.getLabel(rawDict)
        self.getMandatoryMetaData(rawDict)
        self.getOptionalMetaData(rawDict)
        self.getFilters(rawDict)
        self.getClassifiers(rawDict)


    def getClassifiers(self, rawDict):
        if ('classifiers' in rawDict):
            for classifier in rawDict['classifiers']:
                self.classifiers.append(Classifier(classifier))
    def getFilters(self, rawDict):
        if ('filters' in rawDict):
            for filter in rawDict['filters']:
                self.filters.append(Filter(filter))

    def getOptionalMetaData(self, rawDict):
        if('optionalMetaData' in rawDict):
            if not ('main' in rawDict):
                raise Exception('Non-Main data cannot have meta data!')
            for key in rawDict['optionalMetaData']:
                self.optionalMetaData.append(key)
    def getMandatoryMetaData(self, rawDict):
        if('mandatoryMetaData' in rawDict):
            if not ('main' in rawDict):
                raise Exception('Non-Main data cannot have meta data!')
            for key in rawDict['mandatoryMetaData']:
                self.mandatoryMetaData.append(key)

    def getLabel(self, rawDict):
        if('label' in rawDict):
            self.label = rawDict['label']
        else:
            self.label = self.key

    def getMain(self, rawDict):
        if('main' in rawDict):
            self.main = True

    def getAliases(self, rawDict):
        if not ('aliases' in rawDict):
            pass
        else:
            #print(rawDict)
            for alias in rawDict['aliases']:
                #print(alias)
                self.aliases.append(Alias(alias))
