import re
import networkx as nx


class Wire():
	name = "defaultname"
	isInput = False
	isOutput = False
	source = "defaultname"
	ports = []
	level = 0
	

class Gate():
	gtype = "defaulttype"
	name = "defaultname"
	inputport1 = "defaultname"
	inputport2 = "defaultname"
	outputport = "defaultname"
	level = 0
	connected1 = False
	connected2 = False

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
def getfirstlevel(mygraph, gatelist, prevgatelist):
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

def getnextlevel(mygraph, gatelist, prevgatelist):
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
	filePath = "/home/ahmed/Desktop/booth.g.v"
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")

	assignlist = {}
	for x in verilogfile:
		p = re.compile("\s*assign\s*(\s*\S+\s*\S*)\s*=\s*(\s*\S+\s*\S*)\s*;") 
		m = p.match(x)
		if m is not None:
			s1 = ''.join(m.group(1).split())
			s2 = ''.join(m.group(2).split())
			assignlist[s1] = s2
	
	verilogfile.close()

	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")
	

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

	#for j in wiredict:
	#	print (wiredict[j].name+" "+str(wiredict[j].isInput)+" "+str(wiredict[j].isOutput)+" "+wiredict[j].source)

	returnlist = getfirstlevel(G, gatelist, inputdict)
	i = 0
	while(len(gatelist) > returnlist[0]):
		returnlist = getnextlevel(G, gatelist, returnlist[1])
		i = i +1
		
	
	copyGatelist = gatelist
	for i, h in enumerate(copyGatelist):
		if((wiredict[copyGatelist[i].inputport1].isInput == False) and (wiredict[copyGatelist[i].inputport1].isOutput == False)):
			print(wiredict[copyGatelist[i].inputport1].source, 'a')
			copyGatelist[i].inputport1 = wiredict[copyGatelist[i].inputport1].source
		if	(copyGatelist[i].inputport2 is not 'defaultname'):
			if((wiredict[copyGatelist[i].inputport2].isInput == False) and (wiredict[copyGatelist[i].inputport2].isOutput == False)):
				print(wiredict[copyGatelist[i].inputport2].source, 'b')
				copyGatelist[i].inputport2 = wiredict[copyGatelist[i].inputport2].source
		if((wiredict[copyGatelist[i].outputport].isInput == False) and (wiredict[copyGatelist[i].outputport].isOutput == False)):
			print(wiredict[copyGatelist[i].outputport].source, 'c')
			copyGatelist[i].outputport = wiredict[copyGatelist[i].outputport].source

	#for h, z in enumerate(copyGatelist):
		#print(copyGatelist[h].name+" "+copyGatelist[h].gtype+" "+str(copyGatelist[h].level)+" "+str(copyGatelist[h].connected1)+" "+str(copyGatelist[h].connected2)+" "+copyGatelist[h].inputport1+" "+copyGatelist[h].inputport2+" "+copyGatelist[h].outputport)

if __name__ == "__main__":
	main()