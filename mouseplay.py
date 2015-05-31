import datetime
import pygame
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import re
import analysis

clock = pygame.time.Clock()
qwertyString = "qwertyuiopasdfghjklzxcvbnm"
qwertyPositions = [(34, 60)
,
(114, 59)
,
(196, 59)
,
(280, 65)
,
(357, 61)
,
(442, 60)
,
(520, 59)
,
(601, 59)
,
(680, 59)
,
(761, 61)
,
(82, 162)
,
(157, 167)
,
(235, 166)
,
(317, 166)
,
(399, 167)
,
(480, 166)
,
(558, 164)
,
(633, 164)
,
(715, 166)
,
(157, 265)
,
(238, 270)
,
(319, 269)
,
(395, 268)
,
(477, 271)
,
(555, 267)
,
(637, 274)
]

def QwertyOrd(char):
    
    while index < len(qwertyString) and char != qwertyString[index]:
        index += 1
    return index

def Dist(pos1, pos2):
    diff = np.array([pos1[0] - pos2[0], pos1[1] - pos2[1]])
    return np.linalg.norm(diff) 

def Pad(x):
    return '0'*(4-len(str(x))) + str(x)

class FrameData:
    def __init__(self, pos):
        self.position = np.array(pos)
        self.time = datetime.datetime.now()
        self.velocity = 0
        self.accel = 0
        self.closestLetter = 'z'
        self.letterDistance = 0
        self.updateQwertyInfo()
    
    def updateQwertyInfo(self):
        distances = [Dist(self.position, p) for p in qwertyPositions]
        minDistIndex = np.argmin(distances)
        self.closestLetter = qwertyString[minDistIndex]
        self.letterDistance = distances[minDistIndex]
    def getClosestLetter(self):
        return self.closestLetter
    
class SwypeTrajectory:
    def __init__(self, fileName):
        self._fileName = fileName
        self._frameDataList = []
        self.word = ""
    def AddFrame(self, pos):
        newFrame = FrameData(pos)
        self._frameDataList.append(newFrame)
    def Pickle(self):
        pickle.dump( self, open( self._fileName, "wb" ) )
    def Load(self, fileName):
        self = pickle.load( open( fileName, "wb"))
    def GetLetterSequence(self):
        return ''.join([x.closestLetter for x in self._frameDataList])
        
        
def main ():
    pygame.display.set_caption('Testing')
    pygame.init()
    
    screen = pygame.display.set_mode((797,414))
    img = pygame.image.load("swype.png")
    screen.blit(img,(0,0))
    pygame.display.flip()

    linesToDraw = []
    running = True
    recording = False
    oldpos = None

    trajectory = SwypeTrajectory("training/trajectory" + re.sub(r' ', r'_', str(datetime.datetime.now())))

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION and recording == True:
            linesToDraw.append(event.pos)
            trajectory.AddFrame(event.pos) 
            screen.blit(img, (0,0))
            pygame.draw.lines(screen, (255, 127, 80), False, linesToDraw, 4)
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            linesToDraw = [event.pos]
            if recording:
                analysis.AnalyzeTrajectory(trajectory)
                while True:
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        frameData = FrameData(event.pos)
                        if frameData.getClosestLetter() == 's':
                            trajectory.Pickle()
                        break
                        #     break
                        # elif frameData.getClosestLetter() == 'c':
                        #     break
                    elif event.type == pygame.KEYDOWN:
                        trajectory.word += chr(event.key)
                trajectory = SwypeTrajectory("training/trajectory" + re.sub(r' ', r'_', str(datetime.datetime.now())))
            recording = not recording
                

        screen.fill((0, 0, 0))
        clock.tick(120)
        # pygame.display.flip()

if (__name__ == '__main__'):
    main()

