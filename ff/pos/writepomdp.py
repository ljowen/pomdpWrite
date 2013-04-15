from xml.dom.minidom import parseString;
import area as a;
#import argparse;


def np_toStr(fArr) :
	ret = "";
	for i in fArr:
		ret += repr(i) + " ";
	return ret;

## Generate 'land' map of transition probs


## Define ranges of states
Pr_min = 0; #lowest possible error 0 means we are 100% certain of Pc
Pr_max = 3# myLand.xdim ; #largest possible error
GPSstat_max = 3; # Max time we can record before GPS gets a lock
GPSstat_min = -3; # Min locking time 1 -> 1 timestep from action_on
LT_min = 0;
LT_max = GPSstat_max;

myLand = a.make_ten(LT_max);
print myLand;
print "Pc Range " + "x: " + repr(myLand.xdim) + " y: " + repr(myLand.ydim);
## Write Pc stuff (mean location)
Pc_trans ="""
		<CondProb>
			<Var>Pc_now</Var>
			<Parent>Pc_prev</Parent>
			<Parameter type = "TBL">
"""
Pc_enum = "";
for i in range(myLand.xdim):
	for j in range(myLand.ydim):
		Pc_enum += " Pc"+repr(i)+"_" +repr(j) + " ";
		myLand[i,j];
		fsum = 0; # Float sum to check pr adds to 1
		#doneAdd = False;
		for dirn in a.validDirs:
			adj = myLand.get_neighbour(i, j, dirn);
			if(myLand.is_outside(adj[0],adj[1]) == False):
				fsum += float(repr(myLand[i,j].pc_trans[dirn]));
				Pc_trans += """
				<Entry>
				<Instance>"""+"Pc"+repr(i)+"_"+repr(j)+" Pc"+repr(adj[0])+"_"+repr(adj[1])+""" </Instance> 
				<ProbTable>""" + repr(myLand[i,j].pc_trans[dirn]) + """</ProbTable>
				</Entry>
				"""
		#if(fsum != 1):
		#	print "float is " + repr(fsum) + " rem: " + repr(1-fsum);
Pc_trans += """</Parameter>
				</CondProb>""";
'''
## Write Pr stuff (mean error) ########################
'''


Pr_enum = "";
print "Pr Range: " + repr(Pr_min) + " to " + repr(Pr_max);
Pr_trans = """
		<CondProb>
		<Var>Pr_now</Var>
		<Parent>GPS_prev Pr_prev</Parent>
		<Parameter type = "TBL">
""";


for i in range(Pr_min, Pr_max+1):
	Pr_enum += " Pr" + repr(i) + " ";
	if(i < Pr_max - 1):
		Pr_trans += """
			<Entry>
			<Instance>- """ + "Pr" + repr(i) + " Pr" + repr(i+1) + """</Instance>
			<ProbTable> 1 1 0 </ProbTable>
			</Entry>
		""";

	else: #Max error remain stationary
		Pr_trans += """
			<Entry>
			<Instance> - """ + "Pr" + repr(i) + " Pr" + repr(i) + """</Instance>
			<ProbTable> 1 1 0 </ProbTable>
			</Entry>
		""";
		# On Lock -> goto min
Pr_trans += """
			<Entry>
			<Instance>- """ + "*" +" Pr" + repr(Pr_min) + """</Instance>
			<ProbTable> 0 0 1 </ProbTable>
			</Entry>
		""";
Pr_trans += """</Parameter>
				</CondProb>""";
				
				
'''
####GPSstat stuff #####################
'''
GPSstat_enum = '';
GPSstat_trans = """
		<CondProb>
		<Var>GPSstat_now</Var>
		<Parent>GPS_prev GPSstat_prev </Parent>
		<Parameter type = "TBL">
""";

print "GPSstat range: " + repr(GPSstat_min) + " to " + repr(GPSstat_max); 
for i in range(GPSstat_min,GPSstat_max + 1):
	GPSstat_enum += ' GPSstat_' + repr(i) + ' ';
	if(i  < GPSstat_max): ## Increases if ON
		GPSstat_trans += """
				<Entry>
				<Instance> - """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i+1)+"""</Instance>
				<ProbTable> 1 0 0  </ProbTable> 
				</Entry>
				"""; 
	if(i > GPSstat_min): ## Decreases if Off
		GPSstat_trans += """
                <Entry>
                <Instance> - """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i-1)+"""</Instance>
                <ProbTable> 0 1 0 </ProbTable> 
                </Entry>
                """; 
	if(i == GPSstat_max): ## If at max remains the same
		GPSstat_trans += """
				<Entry>
				<Instance> - """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i)+"""</Instance>
				<ProbTable> 1 0 0 </ProbTable> 
				</Entry>
				""";
	if(i == GPSstat_min): ## If at Min and off remain stationary 
		GPSstat_trans += """
				<Entry>
				<Instance> - """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i)+"""</Instance>
				<ProbTable> 0 1 0 </ProbTable> 
				</Entry>
				""";
# RESETS to 0 if lock
GPSstat_trans += """ 
				<Entry>
				<Instance>LOCK """ + ' * ' + " GPSstat_"+repr(0)+"""</Instance>
				<ProbTable> 1 </ProbTable> 
				</Entry>
				"""; 

GPSstat_trans += """</Parameter>
					</CondProb>""";

''' DEFINE TRANSITION FOR LT '''
LT_enum = "LT_none"; # place holder so obs matches un obs
LT_obs_enum = "oLT_none ";

print "LT range: " + repr(LT_min) + " to " + repr(LT_max);
for i in range(LT_min,LT_max+1):
	LT_enum += " LT_"+repr(i)+" ";
	LT_obs_enum += " oLT_" + repr(i) + " ";

'''For each position'''
LT_trans = """
		<CondProb>
		<Var>LT_now</Var>
		<Parent>Pc_prev </Parent>
		<Parameter type = "TBL">""";
for i in range(myLand.xdim):
	for j in range(myLand.ydim):
		LT_trans += """
				<Entry>
				<Instance>"""+"Pc"+repr(i)+"_"+repr(j) + " LT_" + repr(myLand.points[i,j].lt)+""" </Instance>
				<ProbTable> 1 </ProbTable>
				</Entry>
				""";
LT_trans += """ <Entry>
				<Instance> * LT_none </Instance>
				<ProbTable> 0 </ProbTable>
				</Entry>
				</Parameter>
			   </CondProb>""";



LT_obs_func = """
<CondProb>
<Var>LT_obs</Var>
<Parent>GPS_now Pc_now Pr_now</Parent>
<Parameter type="TBL">""";

for i in range(myLand.xdim):
	for j in range(myLand.ydim):
		for k in range(Pr_min,Pr_max+1):
		#	for l in range(LT_min,LT_max):
				ltdic = myLand.get_ELT(i,j,k);
				LT_obs_func += """
				<Entry>
				<Instance>""" + " LOCK " +" Pc"+repr(i)+"_"+repr(j)+" Pr"+repr(k)+" -"+ """</Instance>
				<ProbTable> 0  """ + myLand.get_ELT(i, j, k)["PrStr"] + """</ProbTable>
				</Entry>"""

LT_obs_func += """
				<Entry>
				<Instance>""" + " ON " +"* " + " * "  + " oLT_none " + """</Instance>
				<ProbTable>""" + "1" + """</ProbTable>
				</Entry>"""
LT_obs_func += """
				<Entry>
				<Instance>""" + " OFF " +"* " + " * "  + " oLT_none " + """</Instance>
				<ProbTable>""" + "1" + """</ProbTable>
				</Entry>"""

LT_obs_func += """
</Parameter>
</CondProb> """

''' DEFINE GPS action transitions'''
GPS_enum = "ON OFF LOCK";


GPS_trans = """
	  <CondProb>
		  <Var>GPS_now</Var>
		  <Parent>action_agent LT_prev GPSstat_prev GPS_prev  </Parent>
		  <Parameter type = "TBL">
			  <Entry>
				   <Instance>a_ON * * OFF ON</Instance>
				   <ProbTable>1</ProbTable>
			  </Entry>
			  <Entry>
				   <Instance>a_OFF * * - OFF</Instance>
				   <ProbTable>1 1 1</ProbTable>
			  </Entry>
			  <Entry>
			  		<Instance>a_ON * * LOCK LOCK </Instance>
			  		<ProbTable> 1 </ProbTable>
			  </Entry>
			  <Entry>
			  		<Instance>a_ON LT_none * ON ON </Instance>
			  		<ProbTable> 1 </ProbTable>
			  </Entry>
			  """
# For each GPS_stat / LT combination

for i in range(LT_min,LT_max+1):
	lock_LT_GPSstat_probtable = "";
	on_LT_GPSstat_probtable = "";
	for j in range(GPSstat_min,GPSstat_max+1):
		if(j >= i):
			lock_LT_GPSstat_probtable += " 1 ";
			on_LT_GPSstat_probtable += " 0 ";
		else:
			lock_LT_GPSstat_probtable += " 0 ";
			on_LT_GPSstat_probtable += " 1 ";
	GPS_trans += """
			<Entry>
				<Instance> a_ON """+"LT_"+repr(i) + """ - ON LOCK </Instance>
				<ProbTable>""" + lock_LT_GPSstat_probtable + """</ProbTable>
			</Entry>
			<Entry>
				<Instance> a_ON """+"LT_"+repr(i) + """ - ON ON </Instance>
				<ProbTable>""" + on_LT_GPSstat_probtable + """</ProbTable>
			</Entry>"""

GPS_trans += """			  
		  </Parameter>
	  </CondProb>"""

'''WRITE REWARD FUNCTION'''
Pr_reward = "";
for i in range(Pr_min,Pr_max+1):
	Pr_reward += " " + repr(-2*(i+1));
reward_func = """  

  <RewardFunction>
  <Func>
  <Var>reward_agent</Var>
  <Parent>action_agent Pr_prev </Parent>
  <Parameter type="TBL">
  <Entry>
  <Instance> * - </Instance>
  <ValueTable>""" +  Pr_reward + """</ValueTable></Entry>
  <Entry>
  <Instance> a_ON * </Instance>
  <ValueTable> """ + repr(-4 * (Pr_max/2)) + """</ValueTable></Entry>
  </Parameter>
  </Func>
  </RewardFunction>"""

		
header = """<?xml version="1.0" ?><pomdpx id="autogenerated" version="0.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="pomdpx.xsd">
<Description>This is an auto-generated POMDPX file</Description>
<Discount>0.95</Discount>	"""


xmlStr= (header + """
	  

<Variable>

<StateVar fullyObs="true" vnameCurr="Pc_now" vnamePrev="Pc_prev">
	<ValueEnum>""" + Pc_enum +"""</ValueEnum>
</StateVar>

<StateVar fullyObs="true" vnameCurr="Pr_now" vnamePrev="Pr_prev">
	<ValueEnum>""" + Pr_enum + """ </ValueEnum>
</StateVar>

<StateVar fullyObs="true" vnameCurr="GPSstat_now" vnamePrev="GPSstat_prev">
	<ValueEnum>""" + GPSstat_enum +  """</ValueEnum>
</StateVar>

<StateVar fullyObs="true" vnameCurr="GPS_now" vnamePrev="GPS_prev">
<ValueEnum>""" + GPS_enum + """</ValueEnum>
</StateVar>

<StateVar vnameCurr="LT_now" vnamePrev="LT_prev">
<ValueEnum>""" + LT_enum + """</ValueEnum>
</StateVar>

<ObsVar vname="LT_obs">
<ValueEnum>""" + LT_obs_enum  + """</ValueEnum>
</ObsVar>

<ActionVar vname="action_agent">
<ValueEnum>a_ON a_OFF</ValueEnum>

</ActionVar>
<RewardVar vname="reward_agent"/>
</Variable>

<InitialStateBelief>
<CondProb>
	 <Var>Pc_prev</Var>
	 <Parent>null</Parent>
	 <Parameter type = "TBL"> 
		<Entry>
		<Instance> - </Instance>
		<ProbTable>uniform</ProbTable>
		</Entry>
	</Parameter>
</CondProb>
<CondProb>
	<Var>GPS_prev</Var>
 	<Parent>null</Parent>
 	<Parameter type = "TBL"> 
		 <Entry>
		 <Instance> - </Instance>
		 <ProbTable> 0 1 0 </ProbTable>
		</Entry>
	</Parameter>
</CondProb>
<CondProb>
	<Var>Pr_prev</Var>
	<Parent>null</Parent>
	<Parameter type = "TBL">
		<Entry>
		<Instance> - </Instance>
		<ProbTable> uniform </ProbTable>
		</Entry>
	</Parameter>	
</CondProb>
<CondProb>
	<Var>GPSstat_prev</Var>
	<Parent>null</Parent>
	<Parameter type = "TBL">
		<Entry>
		<Instance> - </Instance>
		<ProbTable> uniform </ProbTable>
		</Entry>
	</Parameter>	
</CondProb>
<CondProb>
	<Var>LT_prev</Var>
	<Parent>null</Parent>
	<Parameter type = "TBL">
		<Entry>
		<Instance> - </Instance>
		<ProbTable> uniform </ProbTable>
		</Entry>
	</Parameter>	
</CondProb>
</InitialStateBelief>

<StateTransitionFunction>
""" + Pc_trans + """
""" + Pr_trans + """
""" + GPSstat_trans + """
""" + LT_trans + """
""" + GPS_trans + """
</StateTransitionFunction>
 
 <ObsFunction>"""
 + LT_obs_func +
 """</ObsFunction>

""" + reward_func + """
  
  </pomdpx>

	"""	);

with open("ff_pos10.pomdpx", "w") as f:
	f.write( xmlStr );
doc = parseString(xmlStr);
quit();
