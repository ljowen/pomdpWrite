import numpy as np;

class AreaPoint:
	def __init__(self):
		self.set_even();

	def set_nesw(self,pn,pe,ps,pw,p0):
		self.pr = {"pn" : pn, "pe" : pe, "ps" : ps, "pw" : pw, "p0" : p0} ;

	def set_even(self):
		self.pr = {"pn" : 0.2, "pe" : 0.2, "ps" : 0.2, "pw" : 0.2, "p0" : 0.2} ;

	def set_edge_even(self, edge):
		self.pr = {"pn" : 0.25, "pe" : 0.25, "ps" : 0.25, "pw" : 0.25, "p0" : 0.25}; 
		if(edge == "n"):
			self.pr["pn"] = 0;
		elif(edge == "e"):
			self.pr["pe"] = 0;
		elif(edge == "s"):
			self.pr["ps"] = 0;
		elif(edge == "w"):
			self.pr["pw"] = 0;
	def set_corner_even(self, corner):
		self.pr = {"pn" : 1.0/3, "pe" : 1.0/3, "ps" : 1.0/3, "pw" : 1.0/3, "p0" : 1.0/3} ;
		if(corner == "ne"):
			self.pr["pn"] = 0;
			self.pr["pe"] = 0;
		elif(corner == "se"):
			self.pr["ps"] = 0;
			self.pr["pe"] = 0;
		elif(corner == "sw"):
			self.pr["pw"] = 0;
			self.pr["ps"] = 0;
		elif(corner == "nw"):
			self.pr["pn"] = 0;
			self.pr["pw"] = 0;


	def set_camp(self):
		self.pr["p0"] = 0.4;
		self.pr["n"] = 0.15;
		self.pr["s"] = 0.15;
		self.pr["e"] = 0.15;
		self.pr["w"] = 0.15;
	def __str__(self):
		return self.pr.__str__();

class Area:
	def __init__(self):
		self.points = {};	
	def __init__(self,xdim,ydim):
		self.points = {};
		self.xdim = xdim;
		self.ydim = ydim;
		for i in range(0,xdim):
			for j in range(0,ydim):
				self.points[i,j] = AreaPoint();
				if(i == 0):
					self.points[i,j].set_edge_even("w");
				elif(i == xdim-1):
					self.points[i,j].set_edge_even("e");
				elif(j == 0):
					self.points[i,j].set_edge_even("s");
				elif(j == ydim-1):
					self.points[i,j].set_edge_even("n");
		self.points[0,0].set_corner_even("sw");
		self.points[0,ydim-1].set_corner_even("nw");
		self.points[xdim-1,0].set_corner_even("se");
		self.points[xdim-1,ydim-1].set_corner_even("ne");

	def __getitem__(self, key):
		return self.points[key];
	def __str__(self):
		retStr = "-" * (self.xdim+2) + "\r\n";
		for y in range(self.ydim-1, -1, -1):
			retStr += "|";
			for x in range(0, self.xdim):
				if(self[x,y].pr["p0"] >= 0.4):
					retStr += "#";
				else:
					retStr += ".";
			retStr += "|\r\n";
		retStr += "-" * (self.xdim+2) + "\r\n";
		return retStr;
def make_ten():
	a = Area(10,10);
	a[6,1].set_camp();
	a[2,7].set_camp();
	return a;
