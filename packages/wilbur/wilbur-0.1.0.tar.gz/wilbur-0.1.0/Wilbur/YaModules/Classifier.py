import numpy as np


class Classifier():
    def __init__(self, rawDict):
        self.name = str(list(rawDict.keys())[0])
        if('min' in rawDict[self.name]):
            self.min = rawDict[self.name]['min']
        else:
            self.min = -np.inf
        if('max' in rawDict[self.name]):
            self.max = rawDict[self.name]['max']
        else:
            self.max = np.inf
        if('invert' in rawDict[self.name]):
            self.invert = False
        else:
            self.invert = True

    def check(self, value):
        return ((self.min<value) and (self.max>value))