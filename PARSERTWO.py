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

def parseInv(gatelist, k, m, verilogfile):
	gatelist.append(Gate())
	gatelist[k].gtype = "INVX1"
	gatelist[k].name = m.group(1)
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
	m = p.match(j)
	gatelist[k].inputport1 = m.group(1)
	returnlist.append(m.group(1))
	j = verilogfile.readline()
	p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
	m = p.match(j)
	gatelist[k].outputport = (m.group(1))
	returnlist.append(m.group(1))
	return returnlist

	

def parseRest(gatedescription, gatelist, k, m, verilogfile):
	gatelist.append(Gate())
	gatelist[k].gtype = gatedescription
	gatelist[k].name = m.group(1)
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
	m = p.match(j)
	gatelist[k].inputport1 = m.group(1)
	returnlist.append(m.group(1))
	j = verilogfile.readline()
	p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
	m = p.match(j)
	gatelist[k].inputport2 = m.group(1)
	returnlist.append(m.group(1))
	j = verilogfile.readline()
	p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
	m = p.match(j)
	gatelist[k].outputport = m.group(1)
	returnlist.append(m.group(1))
	return returnlist
	

def parseFF(gatelist, k, m, verilogfile):
	gatelist.append(Gate())
	gatelist[k].gtype = "DFFPOSX1"
	gatelist[k].name = m.group(1)
	returnlist = [m.group(1)]
	j = verilogfile.readline()
	p = re.compile("\s*\.CLK\((\S+\s*\S*)\),\s*")
	m = p.match(j)
	gatelist[k].inputport1 = m.group(1)
	returnlist.append(m.group(1))
	j = verilogfile.readline()
	p = re.compile("\s*\.D\((\S+\s*\S*)\),\s*")
	m = p.match(j)
	gatelist[k].inputport2 = m.group(1)
	returnlist.append(m.group(1))
	j = verilogfile.readline()
	p = re.compile("\s*\.Q\((\S+\s*\S*)\)\s*")
	m = p.match(j)
	gatelist[k].outputport = (m.group(1))
	returnlist.append(m.group(1))
	return returnlist


def getnextlevel(mygraph, gatelist, prevgatelist):
	c = 0
	nextgatelist = {}
	for i, d in enumerate(gatelist):
		if (gatelist[i].connected1 == False or gatelist[i].connected2 == False):
			for j in prevgatelist:
				if (gatelist[i].inputport1 == prevgatelist[j].name):
					mygraph.add_edge(prevgatelist[j].name, gatelist[i].name)
					mygraph.node[gatelist[i].name]['gtype'] = gatelist[i].gtype
					gatelist[i].level = prevgatelist[j].level + 1
					gatelist[i].connected1 = True
					nextgatelist[gatelist[i].name] = gatelist[i]
					

				if (gatelist[i].inputport2 == prevgatelist[j].name):
					mygraph.add_edge(prevgatelist[j].name, gatelist[i].name)
					gatelist[i].level = prevgatelist[j].level + 1
					mygraph.node[gatelist[i].name]['gtype'] = gatelist[i].gtype
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
	
	

	#########get all wires/inputs/outputs excluding buses
	k =0
	wiredict = {}
	inputdict = {}
	gatelist = []
	for x in verilogfile:
		p = re.compile("\s*wire\s*(\S*);")
		m = p.match(x)
		if m is not None:
			wirex = Wire()
			wirex.name = m.group(1)
			wiredict[m.group(1)] = wirex
		else:
			p = re.compile("\s*input\s*(\S*);")
			m = p.match(x)
			if m is not None:
				wirex = Wire()
				wirex.name = m.group(1)
				wirex.isInput = True
				wirex.level = 1
				wiredict[m.group(1)] = wirex
				inputdict[m.group(1)] = wirex
			else:
				p = re.compile("\s*output\s*(\S*);")
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
									sourcename = parseInv(gatelist, k, m, verilogfile)
									sourcename[2] = ''.join(sourcename[2].split())
									wiredict[sourcename[2]].source = sourcename[0]
									wiredict[sourcename[2]].ports.append(sourcename[1])
									k = k+1
								else:
									p = re.compile("\s*DFFPOSX1\s*(\S+)\s*\(\s*")
									m = p.match(x)
									if m is not None:
										sourcename = parseFF(gatelist, k, m, verilogfile)
										sourcename[3] = ''.join(sourcename[3].split())
										wiredict[sourcename[3]].source = sourcename[0]
										wiredict[sourcename[3]].ports.append(sourcename[1])
										wiredict[sourcename[3]].ports.append(sourcename[2])
										k = k+1
									else:
										p = re.compile("\s*NOR2X1\s*(\S+)\s*\(\s*")
										m = p.match(x)
										if m is not None:
											sourcename = parseRest("NOR2X1",gatelist, k, m, verilogfile)
											sourcename[3] = ''.join(sourcename[3].split())
											wiredict[sourcename[3]].source = sourcename[0]
											wiredict[sourcename[3]].ports.append(sourcename[1])
											wiredict[sourcename[3]].ports.append(sourcename[2])
											k = k+1
										else:
											p = re.compile("\s*XNOR2X1\s*(\S+)\s*\(\s*")
											m = p.match(x)
											if m is not None:
												sourcename = parseRest("XNOR2X1",gatelist, k, m, verilogfile)
												sourcename[3] = ''.join(sourcename[3].split())
												wiredict[sourcename[3]].source = sourcename[0]
												wiredict[sourcename[3]].ports.append(sourcename[1])
												wiredict[sourcename[3]].ports.append(sourcename[2])
												k = k+1
											else:
												p = re.compile("\s*XOR2X1\s*(\S+)\s*\(\s*")
												m = p.match(x)
												if m is not None:
													sourcename = parseRest("XOR2X1",gatelist, k, m, verilogfile)
													sourcename[3] = ''.join(sourcename[3].split())
													wiredict[sourcename[3]].source = sourcename[0]
													wiredict[sourcename[3]].ports.append(sourcename[1])
													wiredict[sourcename[3]].ports.append(sourcename[2])
													k = k+1
												else:
													p = re.compile("\s*AND2X2\s*(\S+)\s*\(\s*")
													m = p.match(x)
													if m is not None:
														sourcename = parseRest("AND2X2",gatelist, k, m, verilogfile)
														sourcename[3] = ''.join(sourcename[3].split())
														wiredict[sourcename[3]].source = sourcename[0]
														wiredict[sourcename[3]].ports.append(sourcename[1])
														wiredict[sourcename[3]].ports.append(sourcename[2])
														k = k+1
													else:
														p = re.compile("\s*NAND2X1\s*(\S+)\s*\(\s*")
														m = p.match(x)
														if m is not None:
															sourcename = parseRest("NAND2X2",gatelist, k, m, verilogfile)
															sourcename[3] = ''.join(sourcename[3].split())
															wiredict[sourcename[3]].source = sourcename[0]
															wiredict[sourcename[3]].ports.append(sourcename[1])
															wiredict[sourcename[3]].ports.append(sourcename[2])
															k = k+1
														else:
															p = re.compile("\s*OR2X2\s*(\S+)\s*\(\s*")
															m = p.match(x)
															if m is not None:
																sourcename = parseRest("OR2X2",gatelist, k, m, verilogfile)
																sourcename[3] = ''.join(sourcename[3].split())
																wiredict[sourcename[3]].source = sourcename[0]
																wiredict[sourcename[3]].ports.append(sourcename[1])
																wiredict[sourcename[3]].ports.append(sourcename[2])
																k = k+1

	########output wire inputs and outputs names
	#for j in wiredict:
		#print (wiredict[j].name+" "+str(wiredict[j].isInput)+" "+str(wiredict[j].isOutput)+" "+wiredict[j].source)
		#for i, x in enumerate(wiredict[j].ports):
		#	print (str(i) +" " +wiredict[j].ports[i])
	
	
	###########################

	
	#for h, z in enumerate(gatelist):
		#print(gatelist[h].gtype+" "+gatelist[h].name+" "+gatelist[h].inputport1+" "+gatelist[h].inputport2+" "+gatelist[h].outputport)
	gatelevellist = []
	gatelevellist.append(inputdict)
	G = nx.DiGraph()
	for j in inputdict:
		G.add_node(inputdict[j].name, gtype = 'Input')
	
	returnlist = getnextlevel(G, gatelist, inputdict)
	print (returnlist[0])
	print (len(gatelist))
	while (len(gatelist) > returnlist[0]):
		returnlist = getnextlevel(G, gatelist, returnlist[1])
		print (returnlist[0])

	
	print("Nodes")
	print (G.nodes())
	print("Edges")
	print (G.edges())



if __name__ == "__main__":
	main()