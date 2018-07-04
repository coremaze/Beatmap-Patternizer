from ExtraMath import *
from OsuConstants import *
import copy
from math import *
class Pattern():
    def __init__(self):
        pass
    def Load(self, nFile):
        from Map import BeatMap
        bm = BeatMap().Load(nFile)
        circles = copy.deepcopy(bm.circles)
        self.circles = circles    
    def Import(self, circles):
        self.circles = copy.deepcopy(circles)
    def Spacing(self):
        space = 0.0
        num_lines = len(self.circles)-1
        for i in range(num_lines):
            circle1 = self.circles[i]
            circle2 = self.circles[i+1]
            space += dist(circle1.Point(), circle2.Point())
        space /= num_lines
        return space
    def FindCenterPoint(self):
        x = average([c.x for c in self.circles])
        y = average([c.y for c in self.circles])
        return (x, y)
    def SetCenterPoint(self, point):
        pattern_center = self.FindCenterPoint()
        for circle in self.circles:
            circle.x = circle.x - pattern_center[0] + point[0]
            circle.y = circle.y - pattern_center[1] + point[1]
    def Copy(self):
        return copy.deepcopy(self)
    def ChangeSpacing(self, newSpacing):
        centerpoint = self.FindCenterPoint()
        ratio = newSpacing/self.Spacing()
        for circle in self.circles:
            circle.x *= ratio
            circle.y *= ratio
        self.SetCenterPoint(centerpoint)
    def Rotate(self, degrees):
        angle = radians(degrees)
        centerPoint = self.FindCenterPoint()
        s = sin(angle)
        c = cos(angle)
        for circle in self.circles:
            circle.x -= centerPoint[0]
            circle.y -= centerPoint[1]
            xnew = circle.x * c - circle.y * s
            ynew = circle.x * s + circle.y * c
            circle.x = xnew + centerPoint[0]
            circle.y = ynew + centerPoint[1]
    def FindNoteAngleFromCenter(self, index):
        center_x, center_y = self.FindCenterPoint()
        circle =  self.circles[index]
        
        delta_x = circle.x - center_x
        delta_y = center_y - circle.y
        theta_radians = atan2(delta_y, delta_x)
        theta_degrees = degrees(theta_radians)
        return theta_degrees
    def FindFirstLastAverageAngle(self):
        first = self.FindNoteAngleFromCenter(0)
        last = self.FindNoteAngleFromCenter(len(self.circles)-1)
        return AverageAngle(first, last)
    def Length(self):
        return len(self.circles)
    def FlipHorizontal(self):
        for circle in self.circles:
            circle.x = WIDTH - circle.x
    def FlipVertical(self):
        for circle in self.circles:
            circle.y = HEIGHT - circle.y

            
            


##p = Pattern()
##p.Load('JOSTARS ~TOMMY, Coda, JIN~ - JoJo Sono Chi no Kioku~end of THE WORLD~ (Atsuro) [single star].osu')
##print(p.Spacing())
##print(p.FindCenterPoint())
##print(p.FindFirstLastAverageAngle())
