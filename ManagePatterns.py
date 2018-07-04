from glob import glob
from os import getcwd
from os.path import join
from Patterns import *
from OsuConstants import *

def LoadPatterns():
    path = join(getcwd(), 'Patterns')

    loadedPatterns = {}
    for f in glob('%s\\*.osu' % path):
        pattern = Pattern()
        pattern.Load(f)
        pattern.SetCenterPoint(CENTER)

        if pattern.Length() not in loadedPatterns:
            loadedPatterns[pattern.Length()] = []

        loadedPatterns[pattern.Length()].append(pattern)

        print('(Length %d) Loaded %s' % (pattern.Length(), f.split('\\')[-1]))

    

    return loadedPatterns

def MinimumPatternLength(patterns):
    return min([k for k in patterns])

def PopSuitablePattern(patterns, length):
    if MinimumPatternLength(patterns) > length:
        return None
    best = None
    for k in patterns:
        if k <= length and (not best or best < k):
            best = k
    bestPattern = patterns[best].pop(0)
    patterns[best].append(bestPattern)
    return bestPattern
    

##patterns = LoadPatterns()
##print(patterns)
##print(MinimumPatternLength(patterns))
##print(PopSuitablePattern(patterns, 4))
