import sys
from ApplyPatterns import ApplyPatterns
from time import sleep

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: Patternize.py <Map file>')
        quit()
        
    try:
        ApplyPatterns(sys.argv[1])
    except Exception as e:
        print(e)
    sleep(5)
        

