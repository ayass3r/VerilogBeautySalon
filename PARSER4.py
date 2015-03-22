#this library must be imported in order to use regex expression
import re

#The Wire Class, all wires, inputs and outputs of the gatelevel netlist will be represented using this
#the attributes and their default values are shown
class Wire():
	name = "defaultname"
	isInput = False
	isOutput = False
	source = "defaultname"
	level = 0

#The Gate Class, all gates in the gatelevel netlist will be represented using this
#the attributes and their default values are shown
class Gate():
	gtype = "defaulttype" #the gate type, ex/ INV, AND, XOR, etc.
	name = "defaultname"  #the unique identifier of the gate
	inputport1 = "defaultname" #the name of the input/gate connected to the first input of the gate
	inputport2 = "defaultname" #the name of the input/gate connected to the second input of the gate
	outputport = "defaultname" #the name of the wire/output connected to the first input of the gate
	level = 0 #the level of the gate
	connected1 = False #boolean needed in the sorting 
	connected2 = False #boolean needed in the sorting 

#function called when a regex expression captures a line of a INVX1 gate, it will read the
# following two lines, capturing data needed to update the gate attributes, and a list is returned to update other data structures
def parseInv(gatelist, k, m, verilogfile, assignlist): 
	gatelist.append(Gate())
	gatelist[k].gtype = "INVX1"
	gatelist[k].name = m.group(1)
	gatelist[k].connected2 = True
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.A\((\S+\s*\S*)\s*\),\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].inputport1 = assignlist[s]
	else:
		gatelist[k].inputport1 = s
	returnlist.append(s)
	j = verilogfile.readline()
	p = re.compile("\s*\.Y\((\S+\s*\S*)\s*\)\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].outputport = assignlist[s]
	else:
		gatelist[k].outputport = s
	returnlist.append(s)
	return returnlist
#same as parseInV, but used for all two input ports except the Flip Flop
def parseRest(gatedescription, gatelist, k, m, verilogfile, assignlist):
	gatelist.append(Gate())
	gatelist[k].gtype = gatedescription
	gatelist[k].name = m.group(1)
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.A\((\S+\s*\S*)\s*\),\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].inputport1 = assignlist[s]
	else:
		gatelist[k].inputport1 = s
	returnlist.append(s)
	j = verilogfile.readline()
	p = re.compile("\s*\.B\((\S+\s*\S*)\s*\),\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].inputport2 = assignlist[s]
	else:
		gatelist[k].inputport2 = s
	returnlist.append(s)
	j = verilogfile.readline()
	p = re.compile("\s*\.Y\((\S+\s*\S*)\s*\)\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].outputport = assignlist[s]
	else:
		gatelist[k].outputport = s
	returnlist.append(s)
	return returnlist
#same as parseFF, but used to for the Flip Flop level
def parseFF(gatelist, k, m, verilogfile, assignlist):
	gatelist.append(Gate())
	gatelist[k].gtype = "DFFPOSX1"
	gatelist[k].name = m.group(1)
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.CLK\((\S+\s*\S*)\s*\),\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].inputport1 = assignlist[s]
	else:
		gatelist[k].inputport1 = s
	returnlist.append(s)
	j = verilogfile.readline()
	p = re.compile("\s*\.D\((\S+\s*\S*)\s*\),\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].inputport2 = assignlist[s]
	else:
		gatelist[k].inputport2 = s
	returnlist.append(s)
	j = verilogfile.readline()
	p = re.compile("\s*\.Q\((\S+\s*\S*)\s*\)\s*")
	m = p.match(j)
	s = ''.join(m.group(1).split())
	if s in assignlist:
		gatelist[k].outputport = assignlist[s]
	else:
		gatelist[k].outputport = s
	returnlist.append(s)
	return returnlist

#pseudo topological sorting, it iterates on all the gates and checks if it connected to an input  and connects it
#it returns the number of gates found to be already connected, and a list (nextgatelist) of all gates found in level 2
def getfirstlevel(gatelist, prevgatelist):
	c = 0
	nextgatelist = {}
	for i, d in enumerate(gatelist):
		if (gatelist[i].connected1 == False or gatelist[i].connected2 == False):
			for j in prevgatelist:
				if (gatelist[i].inputport1 == prevgatelist[j].name and gatelist[i].connected1 == False):
					gatelist[i].level = max(prevgatelist[j].level + 1, gatelist[i].level)
					gatelist[i].connected1 = True
					nextgatelist[gatelist[i].name] = gatelist[i]
										

				if (gatelist[i].inputport2 == prevgatelist[j].name and gatelist[i].connected2 == False):
					gatelist[i].level = max(prevgatelist[j].level + 1, gatelist[i].level)
					gatelist[i].connected2 = True
					nextgatelist[gatelist[i].name] = gatelist[i]
		else:
			c = c + 1			
	returnlist = [c, nextgatelist]
	return returnlist

#pseudo topological sorting, it iterates on all the gates and checks if it is connected to gates in level n (prevgatelis) and connected to it and connects it
#it returns the number of gates found to be already connected, and a list of all gates found in level n +1 (nextgatelist)
def getnextlevel(gatelist, prevgatelist):
	c = 0
	nextgatelist = {}
	for i, d in enumerate(gatelist):
		if (gatelist[i].connected1 == False or gatelist[i].connected2 == False):
			
			for j in prevgatelist:
				if (gatelist[i].inputport1 == prevgatelist[j].outputport and gatelist[i].connected1 == False):
					gatelist[i].level = max(prevgatelist[j].level + 1, gatelist[i].level)
					gatelist[i].connected1 = True
					nextgatelist[gatelist[i].name] = gatelist[i]				
					

				if (gatelist[i].inputport2 == prevgatelist[j].outputport and gatelist[i].connected2 == False):
					gatelist[i].level = max(prevgatelist[j].level + 1, gatelist[i].level)
					gatelist[i].connected2 = True
					nextgatelist[gatelist[i].name] = gatelist[i]
					
		else:
			c = c + 1			
	returnlist = [c, nextgatelist]
	return returnlist

def main():
	#open the file specified by the filePath
	filePath = "/home/ahmed/Desktop/booth.g.v"
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")

	#this loop will capture all assign statements 
	assignlist = {}
	for x in verilogfile:
		p = re.compile("\s*assign\s*(\s*\S+\s*\S*)\s*=\s*(\s*\S+\s*\S*)\s*;") 
		m = p.match(x)
		if m is not None:
			s1 = ''.join(m.group(1).split())
			s2 = ''.join(m.group(2).split())
			assignlist[s1] = s2
	
	verilogfile.close()

	#open the file again in order to capture the wires, inputs, outputs, and gates
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")
	
	#nested if statements needed for capturing, the for loops reads the file line by line	
	k =0
	wiredict = {}
	inputdict = {}
	gatelist = []
	for x in verilogfile:
		p = re.compile("\s*wire\s*(\S*)\s*;") 
		m = p.match(x)
		if m is not None:
			wirex = Wire()
			wirex.name = m.group(1)
			wiredict[m.group(1)] = wirex
		else:
			p = re.compile("\s*input\s*(\S*)\s*;")
			m = p.match(x)
			if m is not None:
				wirex = Wire()
				wirex.name = m.group(1)
				wirex.isInput = True
				wirex.level = 1
				wiredict[m.group(1)] = wirex
				inputdict[m.group(1)] = wirex
			else:
				p = re.compile("\s*output\s*(\S*)\s*;")
				m = p.match(x)
				if m is not None:
					wirex = Wire()
					wirex.name = m.group(1)
					wirex.isOutput = True
					wiredict[m.group(1)] = wirex
				else:
					p = re.compile("\s*wire\s*\[(\d+):\d\]\s*(\S+)\s*;")
					m = p.match(x)
					if m is not None:
						for i in range(int(m.group(1))+1):
							wirex = Wire()
							wirex.name = m.group(2)+"["+str(i)+"]"
							wiredict[wirex.name] = wirex
					else:
						p = re.compile("\s*input\s*\[(\d+):\d\]\s*(\S+)\s*;")
						m = p.match(x)
						if m is not None:
							for i in range(int(m.group(1))+1):
								wirex = Wire()
								wirex.name = m.group(2)+"["+str(i)+"]"
								wirex.isInput = True
								wirex.level = 1
								wiredict[wirex.name] = wirex
								inputdict[wirex.name] = wirex
						else:
							p = re.compile("\s*output\s*\[(\d+):\d\]\s*(\S+)\s*;")
							m = p.match(x)
							if m is not None:
								for i in range(int(m.group(1))+1):
									wirex = Wire()
									wirex.name = m.group(2)+"["+str(i)+"]"
									wirex.isOutput = True
									wiredict[wirex.name] = wirex
							else:
								p = re.compile("\s*INVX1\s*(\S+)\s*\(\s*")
								m = p.match(x)
								if m is not None:
									sourcename = parseInv(gatelist, k, m, verilogfile, assignlist)
									sourcename[2] = ''.join(sourcename[2].split())
									wiredict[sourcename[2]].source = sourcename[0]
									k = k+1
								else:
									p = re.compile("\s*DFFPOSX1\s*(\S+)\s*\(\s*")
									m = p.match(x)
									if m is not None:
										sourcename = parseFF(gatelist, k, m, verilogfile, assignlist)
										sourcename[3] = ''.join(sourcename[3].split())
										wiredict[sourcename[3]].source = sourcename[0]
										k = k+1
									else:
										p = re.compile("\s*NOR2X1\s*(\S+)\s*\(\s*")
										m = p.match(x)
										if m is not None:
											sourcename = parseRest("NOR2X1",gatelist, k, m, verilogfile, assignlist)
											sourcename[3] = ''.join(sourcename[3].split())
											wiredict[sourcename[3]].source = sourcename[0]
											k = k+1
										else:
											p = re.compile("\s*XNOR2X1\s*(\S+)\s*\(\s*")
											m = p.match(x)
											if m is not None:
												sourcename = parseRest("XNOR2X1",gatelist, k, m, verilogfile, assignlist)
												sourcename[3] = ''.join(sourcename[3].split())
												wiredict[sourcename[3]].source = sourcename[0]
												k = k+1
											else:
												p = re.compile("\s*XOR2X1\s*(\S+)\s*\(\s*")
												m = p.match(x)
												if m is not None:
													sourcename = parseRest("XOR2X1",gatelist, k, m, verilogfile, assignlist)
													sourcename[3] = ''.join(sourcename[3].split())
													wiredict[sourcename[3]].source = sourcename[0]
													k = k+1
												else:
													p = re.compile("\s*AND2X2\s*(\S+)\s*\(\s*")
													m = p.match(x)
													if m is not None:
														sourcename = parseRest("AND2X2",gatelist, k, m, verilogfile, assignlist)
														sourcename[3] = ''.join(sourcename[3].split())
														wiredict[sourcename[3]].source = sourcename[0]
														k = k+1
													else:
														p = re.compile("\s*NAND2X1\s*(\S+)\s*\(\s*")
														m = p.match(x)
														if m is not None:
															sourcename = parseRest("NAND2X2",gatelist, k, m, verilogfile, assignlist)
															sourcename[3] = ''.join(sourcename[3].split())
															wiredict[sourcename[3]].source = sourcename[0]
															k = k+1
														else:
															p = re.compile("\s*OR2X2\s*(\S+)\s*\(\s*")
															m = p.match(x)
															if m is not None:
																sourcename = parseRest("OR2X2",gatelist, k, m, verilogfile, assignlist)
																sourcename[3] = ''.join(sourcename[3].split())
																wiredict[sourcename[3]].source = sourcename[0]
																k = k+1

	#output all the wires, inputs, outputs
	for j in wiredict:
		print (wiredict[j].name+" "+str(wiredict[j].isInput)+" "+str(wiredict[j].isOutput)+" "+wiredict[j].source)

	#returns the first level of gates, 
	returnlist = getfirstlevel(gatelist, inputdict)
	i = 0
	#return subsequent levels of gates until all the gates are connected
	while(len(gatelist) > returnlist[0]):
		returnlist = getnextlevel(gatelist, returnlist[1])
		i = i +1
		
	#this format of the gatelist will have the ports of the gates naming the gates connected to it, not the wire names
	copyGatelist = gatelist
	for i, h in enumerate(copyGatelist):
		if((wiredict[copyGatelist[i].inputport1].isInput == False) and (wiredict[copyGatelist[i].inputport1].isOutput == False)):
			copyGatelist[i].inputport1 = wiredict[copyGatelist[i].inputport1].source
		if	(copyGatelist[i].inputport2 is not 'defaultname'):
			if((wiredict[copyGatelist[i].inputport2].isInput == False) and (wiredict[copyGatelist[i].inputport2].isOutput == False)):
				copyGatelist[i].inputport2 = wiredict[copyGatelist[i].inputport2].source
		if((wiredict[copyGatelist[i].outputport].isInput == False) and (wiredict[copyGatelist[i].outputport].isOutput == False)):
			copyGatelist[i].outputport = wiredict[copyGatelist[i].outputport].source

	#Print all the gates with all their attributes
	for h, z in enumerate(copyGatelist):
		print(copyGatelist[h].name+" "+copyGatelist[h].gtype+" "+str(copyGatelist[h].level)+" "+str(copyGatelist[h].connected1)+" "+str(copyGatelist[h].connected2)+" "+copyGatelist[h].inputport1+" "+copyGatelist[h].inputport2+" "+copyGatelist[h].outputport)

if __name__ == "__main__":
	main()