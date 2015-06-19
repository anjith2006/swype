import datetime
import pygame
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import re
import analysis
import math
import numpy as np

qwertyString = "qwertyuiopasdfghjklzxcvbnm"
qwertyPositions = [(61, 88)
,
(182, 93)
,
(313, 96)
,
(437, 96)
,
(564, 98)
,
(683, 97)
,
(816, 93)
,
(940, 92)
,
(1058, 96)
,
(1183, 95)
,
(131, 251)
,
(247, 251)
,
(371, 261)
,
(494, 254)
,
(624, 263)
,
(737, 260)
,
(871, 260)
,
(992, 260)
,
(1111, 261)
,
(253, 412)
,
(376, 417)
,
(502, 418)
,
(621, 419)
,
(743, 417)
,
(861, 418)
,
(988, 422)
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
	
	screen = pygame.display.set_mode((1242,644))
	img = pygame.image.load("swnew.png")
	screen.blit(img,(0,0))
	pygame.display.flip()

	linesToDraw = []
	running = True
	recording = False
	oldpos = None
	last_pos=None


	trajectory = SwypeTrajectory("training/trajectory" + re.sub(r' ', r'_', str(datetime.datetime.now())))

	while running:
		event = pygame.event.poll()
		
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEMOTION and recording == True:
			curr_pos=np.array(event.pos)
			#print "last_pos"
			#print last_pos
			#print "curr_pos"
			#print curr_pos
			if last_pos==None:
					last_pos=curr_pos
			if last_pos!=None:
				
				diff=curr_pos-last_pos
				dist=math.sqrt(diff[0]**2+diff[1]**2)
				#print dist
				if dist>25:
					linesToDraw.append(event.pos)
					trajectory.AddFrame(event.pos) 
					screen.blit(img, (0,0))
					pygame.draw.lines(screen, (255, 127, 80), False, linesToDraw, 4)
					pygame.display.update()
					last_pos=np.array(curr_pos)
					
					
			
			
			
			
			
		elif event.type == pygame.MOUSEBUTTONDOWN: # start and stop
			linesToDraw = [event.pos]
			print "here"
			print recording
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
		# pygame.display.flip()

if (__name__ == '__main__'):
	main()

