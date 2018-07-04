from Patterns import *
from Map import *
from OsuConstants import *
from ManagePatterns import *
from ExtraMath import *
def ApplyPatterns(mapFile):
    beatmap = BeatMap()
    beatmap.Load(mapFile)
    ranges = beatmap.FindSingletaps()

    patternSet = LoadPatterns()
    patternsAdded = 0

    for r in ranges:
        rangelen = r[1] - r[0]

        pattern = PopSuitablePattern(patternSet, rangelen)

        
        if pattern is not None and rangelen >= pattern.Length():
            newrange = [r[0]+pattern.Length(), r[1]]
            if newrange[1] - newrange[0] >= pattern.Length():
                ranges.append(newrange)
        else:
            continue



        mappattern = Pattern()
        mappattern.Import( beatmap.circles[r[0]:r[1]] )
        centerpoint = mappattern.FindCenterPoint()
        
        mapSpacing = mappattern.Spacing()

        newPatternSpacing = pattern.Spacing()
        if mapSpacing < 80:
            continue

        pastcircle = beatmap.circles[r[0]-1]
        futurecircle = beatmap.circles[r[1]]


        normalCandidate = pattern.Copy()
        
        HFlipCandidate = pattern.Copy()
        HFlipCandidate.FlipHorizontal()
        
        VFlipCandidate = pattern.Copy()
        VFlipCandidate.FlipVertical()
        
        patternCandidates = {normalCandidate:0, HFlipCandidate:0, VFlipCandidate:0}

        for newpattern in patternCandidates:
            newpattern.SetCenterPoint(centerpoint)
            newpattern.ChangeSpacing(mapSpacing)
            angle= mappattern.FindFirstLastAverageAngle() - newpattern.FindFirstLastAverageAngle()
            newpattern.Rotate(angle)
            for circle in newpattern.circles:
                circle.Bound()

            firstcircle = newpattern.circles[0]
            lastcircle = newpattern.circles[-1]
            
            pastdist = dist(pastcircle.Point(), firstcircle.Point())
            futuredist = dist(futurecircle.Point(), lastcircle.Point())

            patternCandidates[newpattern] = min([pastdist, futuredist])
        
        newpattern = max(patternCandidates, key = lambda k: patternCandidates[k])


            
        beatmap.PastePattern(newpattern, r)
        patternsAdded += 1

    beatmap.version += ' - Patternized'
    newFile = mapFile[:mapFile.rfind('[')]
    newFile += '[%s].osu' % beatmap.version

    beatmap.Output(newFile)
    print('%d patterns added.' % patternsAdded)
    
        
    
