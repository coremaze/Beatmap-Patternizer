from glob import glob
from os import getcwd
from os.path import join
from Patterns import *
from OsuConstants import *

def LoadPatterns():
    #Grabs patterns from the Patterns folder
    path = join(getcwd(), 'Patterns')

    loadedPatterns = {}
    search_path = join(path, '*.osu') #get all .osu files in that dir
    for f in glob(search_path):
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
    #Patterns are grouped by length
    #move pattern to the back of its list
    bestPattern = patterns[best].pop(0)
    patterns[best].append(bestPattern)
    return bestPattern
    

##patterns = LoadPatterns()
##print(patterns)
##print(MinimumPatternLength(patterns))
##print(PopSuitablePattern(patterns, 4))
