from OsuConstants import *

class HitCircle():
    def __init__(self):
        pass
    def Parse(self, line):
        parameters = line.split(",")
        x, y, time, obType, hitSound = [int(x) for x in parameters[0:5]]
        extras = parameters[5]
        self.x, self.y, self.time, self.obType, self.hitSound, self.extras, self.rawLine = x,y,time,obType,hitSound,extras,line
        return self
    def Output(self):
        if not self.obType & 0x1:
            return self.rawLine
        else:
            return ','.join([str(x) for x in [self.x,self.y,self.time,self.obType,self.hitSound,self.extras]])

    def Point(self):
        return (self.x, self.y)
    def SetPoint(self, point):
        x, y = point
        self.x = x
        self.y = y
    def Bound(self):
        #restrain hitcircles to the playfield.
        #they may have ended up outside the playfield during rotation
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT

class BeatmapLoadError(Exception):
    pass

class BeatMap():
    def __init__(self):
        pass
    def Load(self, nFile):
        with open(nFile, 'rb') as f:
            lines = f.read().decode("UTF-8").split('\r\n')

        if lines[0] != 'osu file format v14':
            print('Unknown .osu format')
            raise BeatmapLoadError

        HitObjectsLocation = lines.index('[HitObjects]')
        TimingPointsLocation = lines.index('[TimingPoints]')

        header = lines[:HitObjectsLocation]
        for line in header:
            if line.startswith('Version:'):
                self.version = line[len('Version:'):]
                break
            
        hitObjects = lines[HitObjectsLocation+1:]
        circles = []
        for line in hitObjects:
            if not line:
                continue
            circle = HitCircle().Parse(line)
            circles.append(circle)

        #using this to figure out how big singletaps should be
        firstTimingPoint = lines[TimingPointsLocation + 1]
        self.milliseconds_per_beat = float(firstTimingPoint.split(',')[1])
        print(f'ms per beat: {self.milliseconds_per_beat} ({(1/self.milliseconds_per_beat)*1000*60} BPM)')
            
        self.header = header
        self.hitObjectsLines = hitObjects
        self.circles = circles
        
        return self
    def Output(self, nFile):
        with open(nFile, 'wb') as f:
            for i in range(len(self.header)):
                if self.header[i].startswith('Version:'):
                    self.header[i] = 'Version:%s' % self.version
                    break
            h = ('\r\n'.join(self.header) + '\r\n').encode('UTF-8')
            f.write(h)
            f.write(('[HitObjects]\r\n').encode('UTF-8'))
            obLines = [x.Output() for x in self.circles]
            f.write(('\r\n'.join(obLines)).encode('UTF-8'))
            f.write('\r\n'.encode('UTF-8'))

    def FindSingletaps(self):
        beat_length = self.milliseconds_per_beat

        singletap_length = beat_length / 2

        singleTapSlowest = int(singletap_length * 1.25)
        singleTapFastest = int(singletap_length * 0.75)
        
##        singleTapSlowest = 225 #Highish bpm
##        singleTapFastest = 114
        
        singleTapRange = range(singleTapFastest, singleTapSlowest+1)
        lastdiff = singletap_length #Just a starting value so we have something to work with on the first note.
        consecitive_singletaps = 0
        ranges = []
        for i in range(len(self.circles)-1):
            
            singletap = False
            thisCircle = self.circles[i]
            nextCircle = self.circles[i+1]
            nextdiff = nextCircle.time - thisCircle.time

            #if not first note
            if i:
                lastCircle = self.circles[i-1]
                lastdiff = thisCircle.time - lastCircle.time

            #this note and the last note are singletaps relative to each other, and this note is not a stream to the next
            if lastdiff in singleTapRange and nextdiff > singleTapFastest:
                singletap = True
                consecitive_singletaps += 1
            #this note is a singletap relative to the next note, and isn't the end of a stream
            elif nextdiff in singleTapRange and lastdiff > singleTapFastest:
                singletap = True
                consecitive_singletaps += 1
            #reset singletap counter due to too high or too low speed
            else:
                consecitive_singletaps = 0

            #ignore everything except hitcircles
            if not thisCircle.obType & 0x1:
                consecitive_singletaps = 0
                singletap = False

            #There could be two sections of singletaps separated by a large space instead of a stream    
            if consecitive_singletaps > 0 and lastdiff > singleTapSlowest:
                consecitive_singletaps = 1

            if consecitive_singletaps == 1:
                ranges.append([i, i+1])
            elif consecitive_singletaps > 1:
                ranges[-1][1]+=1

        return ranges

    def PastePattern(self, pattern, noterange):
        #Copies a pattern's positions to some existing notes in another map
        for i in range(noterange[0], noterange[1]):
            try:
                pCircle = pattern.circles[i-noterange[0]]
            except IndexError:
                break
            self.circles[i].x = pCircle.x
            self.circles[i].y = pCircle.y
        

##            print(singletap, consecitive_singletaps, ranges[-1])
##        print(ranges[:10])

            

##class Pattern():
##    def __init__(self):
##        pass
##    def Load(self, nFile):
##        bm = BeatMap().Load(nFile)
##        circles = bm.circles
##        self.circles = circles            
        
        
##if __name__ == '__main__':
##    from Patterns import Pattern
##
##
##    bm = BeatMap()
##    bm.Load('CYTOKINE - sEE NEW THE WORLD, SHE KNEW THE WORLD - CYTOKINE Remix (Frey) [lUNATIC].osu')
##    ranges = bm.FindSingletaps()
##
##
##
##    p = Pattern()
##    p.Load('JOSTARS ~TOMMY, Coda, JIN~ - JoJo Sono Chi no Kioku~end of THE WORLD~ (Atsuro) [single star].osu')
##
##    for r in ranges:
##        if r[1] - r[0] >= len(p.circles):
##            bm.PastePattern(p, r)
##
##    bm.Output('test.osu')
