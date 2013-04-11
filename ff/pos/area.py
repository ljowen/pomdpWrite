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
ltMAX=9;
ltMIN=0;
class AreaPoint:
	
	def __init__(self,x,y,res,edge,lt): 
		self.x = x;
		self.y = y;
		self.res = res;
		self.pr = {"pn":0,"pne":0,"pe":0,"pse":0,"ps":0,"pse":0,"ps":0,"psw":0,"pw":0,"pnw":0};
		self.lt = lt;
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
		
	def set_lt(self,lt):
		self.lt = lt;
	
	def __str__(self):
		return "PR: " + self.pr.__str__() + " LT: " + repr(self.lt);
	

class Area:
		
	def __init__(self,xdim,ydim):
		self.points = {};
		self.xdim = xdim;
		self.ydim = ydim;
		for i in range(0,xdim):
			for j in range(0,ydim):
				if(i == 0):
					self.points[i,j] = AreaPoint(i,j,False,"pw",0);
				elif(i == xdim-1):
					self.points[i,j] = AreaPoint(i,j,False,"pe",0);
				elif(j == 0):
					self.points[i,j] = AreaPoint(i,j,False,"ps",0);
				elif(j == ydim-1):
					self.points[i,j] = AreaPoint(i,j,False,"pn",0);
				else:
					self.points[i,j] = AreaPoint(i,j,False,False,0);
				self.points[i,j].lt = rnd.randint(0,ltMAX);
				
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
	
	def get_numcells_pr(self,x,y,Pr):
		totalCells = 0;
		for i in range(x - Pr, x + Pr+1):
			for j in range(y - Pr, y + Pr+1): # For each position
				if(self.is_outside(i,j) == False):
					totalCells += 1;
		return totalCells;
	
	def get_ELT(self,x,y,Pr):
		outDic = {};
		prStr = "";
#		totalCells = (2*Pr + 1) ** 2;
		totalCells = self.get_numcells_pr(x,y,Pr);
		prSum = 0;
		for lt_val in range(ltMIN,ltMAX+1): # For each value of LT
			lt_sum = 0;
			for i in range(x - Pr, x + Pr+1):
				for j in range(y - Pr, y + Pr+1): # For each position
					if(self.is_outside(i,j) == False):# if pos valid
					#	if(lt_val == ltMIN):
					#		print "i"+repr(i) + " j"+repr(j);
						
						if (self.points[i,j].lt == lt_val):#if lt matches
							#print "at " +repr(i) + " " + repr(j) + ": " + repr(lt_val);
							lt_sum += 1;
			outDic[lt_val] = float(lt_sum)/totalCells ;
			if(lt_val < ltMAX):
				prStr += repr(outDic[lt_val]) + " ,";
			else:
				prStr += repr(outDic[lt_val]); 
			prSum += outDic[lt_val];
		outDic["Total"] = totalCells;	
		outDic["Prsum"] = prSum;
		outDic["PrStr"] = prStr;
		return outDic;
	
		
	
	
def make_ten():
	a = Area(10,10);
	a[6,1].set_res(False);
	a[2,7].set_res(False);
	return a;

def str_index(dic):
	a = dic.values();
	outStr = "";
	for i in a:
		outStr += repr(i) + " ";
	return outStr;
		
	
