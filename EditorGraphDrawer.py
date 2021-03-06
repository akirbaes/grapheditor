try:
	import Tkinter as Tk
except ImportError:
	import tkinter as Tk

margin=30

class NodeDrawing:
	def __init__(self,x,y,canvas,empty=False,content=""):
		self.content="5"
		self.canvas=canvas
		self.x=x 
		self.y=y 

		self.empty=empty
		
		self.lowerbound = margin
		self.upperbound = int(self.canvas.cget("width"))-margin
		
		self.listeners=[]
		
		self.generateDrawing()
		
	def move(self,x,y):
		self.x=min(self.upperbound,max(self.lowerbound,x)) 
		self.y=min(self.upperbound,max(self.lowerbound,y))
		self.canvas.coords(self.oval,self.ovalCoords())
		self.canvas.coords(self.text,(self.x,self.y))
		
		self.notifyListeners("moved")
		
	def isMine(self,shape):
		return self.oval==shape or self.text==shape
		
	def isMyNode(self,realNode):
		return self.realNode == realNode
		
	def generateDrawing(self):
		if(self.empty):
			self.oval=self.canvas.create_oval(self.ovalCoords(),activefill="red")
		else:
			self.oval=self.canvas.create_oval(self.ovalCoords(),fill="pink",activefill="red")
		self.text=self.canvas.create_text((self.x,self.y),text=self.content)
		
	def ovalCoords(self):
		return (self.x-10,self.y-10,self.x+10,self.y+10)
	
	def addListener(self,listener):
		self.listeners.append(listener)
	
	def removeListener(self,listener):
		self.listeners.remove(listener)
		
	def notifyListeners(self,message,argument=None):
		for listener in self.listeners:
			listener.notify(message,argument)
	
	def destroyNode(self):
		self.notifyListeners("destroy")
		self.canvas.delete(self.oval)
		self.canvas.delete(self.text)
		
	def transfer(self,other):
		self.notifyListeners("transfer",(self,other))
		self.canvas.delete(self.oval)
		self.canvas.delete(self.text)
	
		

def generateLines(canvas,nodeslist,adjacence):
	for i in range(len(nodeslist)):
			for j in range(i+1,len(nodeslist)):
				n1 = nodeslist[i]
				n2 = nodeslist[j]
				if(adjacence[i][j]):
					LineDrawing(n1,n2,canvas)
					
					
"""
class NodeLines:
	def __init__(self,canvas,nodeslist=[],adjacence=[[]]):
		self.nodes=nodeslist
		#self.linespos=[]
		self.lines = []
		self.canvas=canvas
		self.adjacence=adjacence
		self.generateLines()
	
		
	def addNode(self,node):
		self.nodes.append(node)
		
	def removeNode(self,node):
		self.nodes.remove(node)
		
	def generateLines(self):
		linespos = []
		
		for i in range(len(self.nodes)):
			for j in range(i+1,len(self.nodes)):
				p1 = self.nodes[i]
				p2 = self.nodes[j]
				if(self.adjacence[i][j]):
					linespos.append((p1.x,p1.y,p2.x,p2.y))
				
		for linepos in linespos:
			self.fatLines.append(self.canvas.create_line(linepos,width=8,fill="grey"))
			self.thinLines.append(self.canvas.create_line(linepos,width=6,fill="pink"))
	
	def drawLines(self):
		
		counter=0
		
		for i in range(len(self.nodes)):
			for j in range(i+1,len(self.nodes)):
				p1 = self.nodes[i]
				p2 = self.nodes[j]
				if(self.adjacence[i][j]):
					self.canvas.coords(self.fatLines[counter],(p1.x,p1.y,p2.x,p2.y))
					self.canvas.coords(self.thinLines[counter],(p1.x,p1.y,p2.x,p2.y))
					counter+=1
		
		
		#for line in self.lines:
		#	self.canvas.delete(line)

"""

class LineDrawing:
	def __init__(self,node1,node2,canvas,distance=-1):
		#distance -1: à la création
		#distance -2: update
		self.nodes=[node1,node2]
		
		
		self.canvas=canvas
		node1.addListener(self)
		node2.addListener(self)
		
		self.fatlLine=None
		self.thinLine=None
		#self.dots=[]
		
		self.generate()
		#if(distance==-1):
		#	self.distance=self.lineDist()
		#else:
		#	self.distance=distance
		
	def redraw(self):
		self.canvas.coords(self.fatlLine,self.lineCoords())
		self.canvas.coords(self.thinLine,self.lineCoords())
		
		#if(abs(self.lineDist()-self.distance)>4):
		#	self.canvas.itemconfig(self.thinLine,dash=min(255,max(1,int(6*self.lineDist()/max(1,self.distance)))))
		#else:
		#	self.canvas.itemconfig(self.thinLine,dash=[])
		#draw dots
		
	def generate(self):
		if(not self.thinLine):
			self.fatlLine=self.canvas.create_line(self.lineCoords(),width=8,fill="grey")
			self.thinLine=self.canvas.create_line(self.lineCoords(),width=6,fill="pink")#,dash=6)
		else:
			pass
			
	def lineCoords(self):
		return (self.nodes[0].x,self.nodes[0].y,self.nodes[1].x,self.nodes[1].y)
		
	def lineDist(self):
		x1,y1,x2,y2=self.lineCoords()
		
		return ((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))**0.5

	def setRealDist(self):
		self.distance=self.lineDist()

	def setDist(self,dist):
		self.distance=dist

	def notify(self,message,argument=None):
		if(message=="destroy"):
			pass
			self.nodes[1].removeListener(self)
			self.nodes[0].removeListener(self)
			self.canvas.delete(self.fatLine)
			self.canvas.delete(self.thinLine)
			self.fatLine=None
			self.thinLine=None
		elif(message=="transfer"):
			print(self.nodes)
			oldnode,newnode=argument
			newnode.addListener(self)
			self.nodes.remove(oldnode)
			oldnode.removeListener(self)
			self.nodes.append(newnode)
			self.redraw()
			
			
		elif(message=="regenerate"):
			pass
		else:
			self.redraw()
		
