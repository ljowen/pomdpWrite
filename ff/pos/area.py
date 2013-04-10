#import numpy as np;
import random as rnd;
validDirs = ("pn","pne","pe","pse","ps","psw","pw","pnw","p0");
validCross = ("pn","pe","ps","pw");
validDiag = ("pne","pse","psw","pnw");
validEdge = ("pn","pne","pe","pse","ps","psw","pw","pnw");
validMoves = {
				"pn" : ("ps","pe","pw","pse","psw"),	 #edge : valid
				"pne" : ("ps","psw","pw"),
				"pe" : ("pn","ps","psw","pw","pnw"),
				"pse" : ("pn","pw","pnw"),
				"ps" : ("pn","pne","pe","pw","pnw"),
				"psw" : ("pn","pne","pe"),
				"pw" : ("pn","pne","pe","pse","ps"),
				"pnw" : ("pe","pse","ps")
				}; 

class AreaPoint:
	
	def __init__(self,x,y,res,edge): 
		self.x = x;
		self.y = y;
		self.res = res;
		self.pr = {"pn":0,"pne":0,"pe":0,"pse":0,"ps":0,"pse":0,"ps":0,"psw":0,"pw":0,"pnw":0};

		if(res == True):
			self.set_res(edge);
		else:
			self.set_even(edge);

	def set_even(self,edge):
		self.set_zero();
		if(edge == False):
			for allowed in validDirs:
				self.pr[allowed] = 1.0/9;
		elif(edge in validCross):
			for allowed in validMoves[edge]:
				self.pr[allowed] = 1.0/6;
				self.pr["p0"] = 1.0/6;
		elif(edge in validDiag):
			for allowed in validMoves[edge]:
				self.pr[allowed] = 1.0/4;
				self.pr["p0"] = 1.0/4;
					
	def set_res(self,edge):
		self.set_zero();
		self.res = True;
		if(edge == False):
			for allowed in validDirs:
				self.pr[allowed] = 0.5/9;
				self.pr["p0"] = 0.5;
		elif(edge in validCross):
			for allowed in validMoves[edge]:
				self.pr[allowed] = 0.5/5;
				self.pr["p0"] = 0.5;
		elif(edge in validDiag):
			for allowed in validMoves[edge]:
				self.pr[allowed] = 1.0/3;
				self.pr["p0"] = 0.5;
	
	def set_zero(self):
		for i in validDirs:
			self.pr[i] = 0;
		
	def is_valid(self):
		sump = 0;
		for i in validDirs:
			sump += self.pr[i];
		if(sump == 1):
			return True;
		else:
			return False;
	
	def __str__(self):
		return self.pr.__str__();
	

class Area:
		
	def __init__(self,xdim,ydim):
		self.points = {};
		self.xdim = xdim;
		self.ydim = ydim;
		for i in range(0,xdim):
			for j in range(0,ydim):
				if(i == 0):
					self.points[i,j] = AreaPoint(i,j,False,"pw");
				elif(i == xdim-1):
					self.points[i,j] = AreaPoint(i,j,False,"pe");
				elif(j == 0):
					self.points[i,j] = AreaPoint(i,j,False,"ps");
				elif(j == ydim-1):
					self.points[i,j] = AreaPoint(i,j,False,"pn");
				else:
					self.points[i,j] = AreaPoint(i,j,False,False);
				
		self.points[0,0].set_even("psw");
		self.points[0,ydim-1].set_even("pnw");
		self.points[xdim-1,0].set_even("pse");
		self.points[xdim-1,ydim-1].set_even("pne");
		
	def set_res_random(self, numRes):
		for i in range(numRes):
			newResX =1;
			newResY =1;
			while(newResX > 0 and newResX < self.xdim-1 and newResY > 0 and newResY < self.ydim-1 ):
				newResX = rnd.randint(0,self.xdim-1);
				newResY = rnd.randint(0,self.ydim-1);
				self.points[newResX,newResY].set_res(False);
	
	def validate(self):
		for i in range(0,self.xdim):
			for j in range(0,self.ydim):
				pt = self.points[i,j];
				sum = 0;
				for d in validDirs:
					sum += pt.pr[d];
				if(round(sum,1) > 1.0):
					return "Validate failed on pt: "+repr(i)+"," + repr(j)+" Sum:" + repr(sum);
		return True;

	def __getitem__(self, key):
		return self.points[key];
	
	def __str__(self):
		retStr = "-" * (self.xdim+2) + "\r\n";
		for y in range(self.ydim-1, -1, -1):
			retStr += "|";
			for x in range(0, self.xdim):
				if(self[x,y].res == True):
					retStr += "#";
				else:
					retStr += ".";
			retStr += "|\r\n";
		retStr += "-" * (self.xdim+2) + "\r\n";
		return retStr;
	
	def is_edge(self,x,y):
		if(x == 0): 
			return True;
		elif(y == 0):
			return True;
		elif(x == (self.xdim -1)):
			return True;
		elif(y == (self.ydim -1)):
			return True;
		return False;
	
	def is_outside(self,x,y):
		if(x < 0): 
			return True;
		elif(y < 0):
			return True;
		elif(x > (self.xdim -1)):
			return True;
		elif(y > (self.ydim -1)):
			return True;
		return False;
	
	def get_dir_add(self,direction):
		if(direction == "pn"):
			return (0,1);
		if(direction == "pne"):
			return (1,1);
		if(direction == "pe"):
			return (1,0);
		if(direction == "pse"):
			return (1,-1);
		if(direction == "ps"):
			return (0,-1);
		if(direction == "psw"):
			return (-1,-1);
		if(direction == "pw"):
			return (-1,0);
		if(direction == "pnw"):
			return (-1,1);
		else:
			return (0,0);
		
	def get_neighbour(self,x,y,direction):
		modifier = self.get_dir_add(direction);
		return(x+modifier[0], y+modifier[1]);
		
		
	
	
def make_ten():
	a = Area(10,10);
	a[6,1].set_res(False);
	a[2,7].set_res(False);
	return a;
