from xml.dom.minidom import parseString;
import area as a;
#import argparse;


def np_toStr(fArr) :
	ret = "";
	for i in fArr:
		ret += repr(i) + " ";
	return ret;

## Generate 'land' map of transition probs

myLand = a.make_ten();
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
		for dirn in a.validDirs:
			adj = myLand.get_neighbour(i, j, dirn);
			if(myLand.is_outside(adj[0],adj[1]) == False):
				Pc_trans += """
				<Entry>
				<Instance>"""+"Pc"+repr(i)+"_"+repr(j)+" Pc"+repr(adj[0])+"_"+repr(adj[1])+""" </Instance> 
				<ProbTable>""" + repr(myLand[i,j].pr[dirn]) + """</ProbTable>
				</Entry>
				"""
Pc_trans += """</Parameter>
				</CondProb>""";
'''
## Write Pr stuff (mean error) ########################
'''

Pr_min = 0; #lowest possible error 0 means we are 100% certain of Pc
Pr_max = 4# myLand.xdim ; #largest possible error
Pr_enum = "";
print "Pr Range: " + repr(Pr_min) + " to " + repr(Pr_max);
Pr_trans = """
		<CondProb>
		<Var>Pr_now</Var>
		<Parent>GPS_prev Pr_prev</Parent>
		<Parameter type = "TBL">
""";


for i in range(Pr_min, Pr_max):
	Pr_enum += " Pr" + repr(i) + " ";
	if(i > Pr_min): 
		Pr_trans += """
			<Entry>
			<Instance>LOCK """ + "Pr" + repr(i) + " Pr" + repr(i-1) + """</Instance>
			<ProbTable> 1 </ProbTable>
			</Entry>
		""";
	else: # Min error, remain stationary 
		Pr_trans += """
			<Entry>
			<Instance>LOCK """ + "Pr" + repr(i) + " Pr" + repr(i) + """</Instance>
			<ProbTable> 1 </ProbTable>
			</Entry>
		""";
	if(i < Pr_max - 1):
		Pr_trans += """
			<Entry>
			<Instance>ON """ + "Pr" + repr(i) + " Pr" + repr(i+1) + """</Instance>
			<ProbTable> 1 </ProbTable>
			</Entry>
		""";
		Pr_trans += """
			<Entry>
			<Instance>OFF """ + "Pr" + repr(i) +" Pr" + repr(i+1) + """</Instance>
			<ProbTable> 1 </ProbTable>
			</Entry>
		""";
	else: #Max error remain stationary
		Pr_trans += """
			<Entry>
			<Instance>ON """ + "Pr" + repr(i) + " Pr" + repr(i) + """</Instance>
			<ProbTable> 1 </ProbTable>
			</Entry>
		""";
		Pr_trans += """
			<Entry>
			<Instance>OFF """ + "Pr" + repr(i) +" Pr" + repr(i) + """</Instance>
			<ProbTable> 1 </ProbTable>
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
GPSstat_max = 5; # Max time we can record before GPS gets a lock
GPSstat_min = -5; # Min locking time 1 -> 1 timestep from action_on
for i in range(GPSstat_min,GPSstat_max + 1):
	GPSstat_enum += ' GPSstat_' + repr(i) + ' ';
	if((i + 1) < GPSstat_max): ## Increases if ON
		GPSstat_trans += """
				<Entry>
				<Instance>OFF """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i+1)+"""</Instance>
				<ProbTable> 0 </ProbTable> 
				</Entry>
				"""; 
		GPSstat_trans += """
				<Entry>
				<Instance>ON """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i+1)+"""</Instance>
				<ProbTable> 1 </ProbTable> 
				</Entry>
				""";               
	elif(i > GPSstat_min + 1): ## Decreases if Off
		GPSstat_trans += """
                <Entry>
                <Instance>OFF """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i-1)+"""</Instance>
                <ProbTable> 1 </ProbTable> 
                </Entry>
                """; 
		GPSstat_trans += """
                <Entry>
                <Instance>ON """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i-1)+"""</Instance>
                <ProbTable> 0 </ProbTable> 
                </Entry>
                """; 
	else: ## If at max remains the same
		GPSstat_trans += """
				<Entry>
				<Instance>OFF """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i)+"""</Instance>
				<ProbTable> 1 </ProbTable> 
				</Entry>
				"""; 
		GPSstat_trans += """
				<Entry>
				<Instance>ON """ + 'GPSstat_'+repr(i) + " GPSstat_"+repr(i)+"""</Instance>
				<ProbTable> 1 </ProbTable> 
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
LT_enum = "";
LT_obs_enum = "";
LT_min = 0;
LT_max = GPSstat_max + abs(GPSstat_min);
print "LT range: " + repr(LT_min) + " to " + repr(LT_max);
for i in range(0,(GPSstat_max + abs(GPSstat_min))):
	LT_enum += " LT_"+repr(i)+" ";
	LT_obs_enum += " oLT_" + repr(i) + " ";

'''For each position'''
LT_trans = """
		<CondProb>
		<Var>LT_now</Var>
		<Parent>Pc_now </Parent>
		<Parameter type = "TBL">""";
for i in range(myLand.xdim):
	for j in range(myLand.ydim):
		LT_trans += """
				<Entry>
				<Instance>"""+"Pc"+repr(i)+"_"+repr(j) + " LT_" + repr(myLand.points[i,j].lt)+""" </Instance>
				<ProbTable> 1 </ProbTable>
				</Entry>
				""";
LT_trans += """</Parameter>
			   </CondProb>""";



LT_obs_func = """
<CondProb>
<Var>LT_obs</Var>
<Parent>LT_now Pc_now  Pr_now</Parent>
<Parameter type="TBL">""";

for i in range(myLand.xdim):
	for j in range(myLand.ydim):
		for k in range(Pr_min,Pr_max):
			for l in range(LT_min,LT_max):
				ltdic = myLand.get_ELT(i,j,k);
				LT_obs_func += """
				<Entry>
				<Instance>""" + "-" + " Pc"+repr(i)+"_"+repr(j)+" Pr"+repr(k)+" oLT_"+repr(l) + """</Instance>
				<ProbTable>""" + myLand.get_ELT(i, j, k)["PrStr"] + """</ProbTable>
				</Entry>"""
				
LT_obs_func += """
</Parameter>
</CondProb> """

		
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
<ValueEnum>ON OFF LOCK</ValueEnum>
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
      <CondProb>
          <Var>GPS_now</Var>
          <Parent>action_agent GPS_prev </Parent>
          <Parameter type = "TBL">
              <Entry>
                   <Instance>a_ON ON ON</Instance>
                   <ProbTable>1</ProbTable>
              </Entry>
              <Entry>
                   <Instance>a_ON OFF ON</Instance>
                   <ProbTable>1</ProbTable>
              </Entry>
              <Entry>
                   <Instance>a_OFF OFF OFF</Instance>
                   <ProbTable>1</ProbTable>
              </Entry>
              <Entry>
                   <Instance>a_OFF ON OFF</Instance>
                   <ProbTable>1</ProbTable>
              </Entry>
              <Entry>
              		<Instance>a_ON LOCK - </Instance>
              		<ProbTable>0.5 0 0.5</ProbTable>
              </Entry>
              <Entry>
                    <Instance>a_OFF LOCK  - </Instance>
                    <ProbTable>0 1 0</ProbTable>
              </Entry>
          </Parameter>
      </CondProb>
 </StateTransitionFunction>
 
 <ObsFunction>"""
 + LT_obs_func +
 """</ObsFunction>

 <RewardFunction>
  
  <Func>
  <Var>reward_agent</Var>
  <Parent>action_agent Pr_prev</Parent>
  <Parameter type="TBL">
  <Entry>
  <Instance>a_ON Pr1 </Instance>
  <ValueTable> 1.0 </ValueTable></Entry>
  <Entry>
  <Instance>a_OFF *  </Instance>
  <ValueTable> 0.0 </ValueTable></Entry>
  </Parameter>
  </Func>
  </RewardFunction></pomdpx>

	"""	);

with open("ff_pos10.pomdpx", "w") as f:
	f.write( xmlStr );
doc = parseString(xmlStr);
quit();
