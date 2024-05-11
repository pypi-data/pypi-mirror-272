import numpy as np


class Filter():
    def __init__(self, rawDict):
        self.type = str(list(rawDict.keys())[0])
        validScopes = ['pre', 'post', 'any']
        if(self.type == 'value'):
            if('min' in rawDict[self.type]):
                self.min = rawDict[self.type]['min']
            else:
                self.min = -np.inf
            if('max' in rawDict[self.type]):
                self.max = rawDict[self.type]['max']
            else:
                self.max = np.inf
            if('invert' in rawDict[self.type]):
                self.invert = False
            else:
                self.invert = True
        elif(self.type == 'file'):
            self.pattern = rawDict[self.type][0]
            if(len(rawDict[self.type])>1):
                self.scope = rawDict[self.type][1]
            else:
                self.scope = 'any'
            if(self.scope not in validScopes):
                raise ValueError('Invalid file filter scope specified')
        else:
            raise TypeError('Invalid filter specification')

    def __str__(self):
        rstring = '\n### Filter ###\n'
        if(self.type == 'value'):
            rstring += 'Type: Value\n - Max: '+str(self.min)+'\n - Min: '+str(self.max)
        elif(self.type == 'file'):
            rstring += 'Type: File Name\n - Pattern: '+self.pattern+'\n - Scope: '+self.scope

        rstring += '\n#############\n'
        return rstring

    def checkValue(self, value):
        if(self.type == 'file'):
            raise TypeError('Non-value filter')
        try:
            numVal = float(value)
        except:
            raise ValueError('Invalid input type for Value filter')
        return ((self.min<numVal) and (self.max>numVal))

    def checkFile(self, fileName):
        if(self.type == 'value'):
            raise ValueError('Non-file filter')

        fileVal = str(fileName).upper()

        if(self.scope=='pre'):
            return fileVal.startswith(self.pattern.upper())
        elif(self.scope=='post'):
            return fileVal.endswith(self.pattern.upper())
        elif(self.scope=='any'):
            return (self.pattern.upper() in fileVal)