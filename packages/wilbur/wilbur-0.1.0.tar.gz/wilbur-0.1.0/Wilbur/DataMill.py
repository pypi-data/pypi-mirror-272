from .YaModules import *
import pandas as pd
import os


class DataMill:

    def __init__(self, dataRoot: str, schemes, includeFilesInData= True):
        self.dataRoot = dataRoot
        self.schemes = schemes
        self.cols = []
        self.grist = []
        self.usedFiles = 0
        self.totalFiles = 0
        self.includeFilesInData = includeFilesInData
        self.mainSchema = []
        for scheme in self.schemes.values():
            self.mainSchema.append(scheme.label)

        self.mainDataFrame = pd.DataFrame(columns=self.mainSchema)
        self.process()
        #self.generateSchema()

    def generateSchema(self):
        for scheme in self.schemes:
            self.cols.append(scheme.label)
        if(self.includeFilesInData):
            self.cols.append('Original File Path')

    def checkDFSchema(self, dataFrame):
        # Get mandatory values from main scheme
        # Create list of top level scheme keys to check for
        # Iterate over these keys and their aliases, check for presence in the imported dataframe
        # Return True when detected & 'or' all values within a given alias-space to return the valid stuff
        validassess = []
        columns = []
        originalSchema = []
        newSchema = []
        for scheme in self.schemes.values():
            if(scheme.main):
                columns.append(scheme.key)
                for key in scheme.mandatoryMetaData:
                    columns.append(key)
                break
        for column in columns:
            validAlias = []
            newSchema.append(self.schemes[column].label)
            for alias in self.schemes[column].aliases:
                if(alias.representation in dataFrame.columns):
                    validAlias.append(True)
                    originalSchema.append(alias.representation)
            validassess.append(any(validAlias))
        return all(validassess), originalSchema, newSchema

    def checkKey(self, key, dataFrame):
        return key in dataFrame.index
    def process(self):
        # Scan Files/filter based on file discriminators

            # Sanitize files & scan headers for mandatory/optional params

                # Add to datastructure


        for root, dirs, files in os.walk(self.dataRoot):
            for file in files:
                self.totalFiles += 1

                # Check file validity
                validassess = []
                for scheme in self.schemes.values():
                    for filter in scheme.filters:
                        try:
                            validassess.append(filter.checkFile(file))
                        except TypeError:
                            validassess.append(True)
                valid = all(validassess)
                if (valid):
                    #print(file)
                    #processValid
                    filePath = os.path.join(root, file)

                    try:
                        df = pd.read_csv(filePath)
                        validSchema, originalSchema, newSchema = self.checkDFSchema(df)
                        if(validSchema):
                            intermediaDataFrame = df[originalSchema]
                            mapper = {}
                            for ocol,ncol in zip(originalSchema, newSchema):
                                mapper.update({ocol:ncol})


                            self.mainDataFrame = pd.concat(
                                [self.mainDataFrame,intermediaDataFrame.rename(columns=mapper, inplace=False)],
                                ignore_index=True)
                    except pd.errors.ParserError:
                        #print('Excepting')
                        pass