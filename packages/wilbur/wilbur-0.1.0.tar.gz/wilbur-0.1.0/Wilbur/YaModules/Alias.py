class Alias():
    def __init__(self, rawDict):
        #print(rawDict)

        self.representation = list(rawDict.keys())[0]
        self.scale = rawDict[self.representation]
        if not type(self.scale) == int:
            self.scale = 1
    def __str__(self):
        rstring = '\n### Alias ###\n'
        rstring += 'Representation: '+self.representation+'\n'
        rstring += 'Relative Scale: '+str(self.scale)
        rstring += '\n#############\n'
        return rstring

    def checkMatch(self, value):
        return value.upper() == self.representation.upper()

    def scaleColumn(self, data):
        scaledData = []
        if(self.scale==1):
            return data
        for value in data:
            scaledData.append(value*self.scale)
        return scaledData