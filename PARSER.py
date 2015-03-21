import re

class Input():
	name = "defaultname"
	ports = []

class Output():
	name = "defaultname"
	ports = []

class Wire():
	name = "defaultname"
	ports = []

class Gate():
	gtype = "defaulttype"
	name = "defaultname"
	inputport1 = "defaultname"
	inputport2 = "defaultname"
	inputport3 = "defaultname"
	outputport = "defaultname"

def main():
	filePath = "/home/ahmed/Desktop/6502_cpu.g.v"
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")
	
	

	#########get all wires/inputs/outputs excluding buses
	wirelist = []
	inputlist = []
	outputlist = []
	for x in verilogfile:
		p = re.compile("\s*wire\s*(\S*);")
		m = p.match(x)
		if m is not None:
			wirex = Wire()
			wirex.name = m.group(1)
			wirelist.append(wirex)
		else:
			p = re.compile("\s*input\s*(\S*);")
			m = p.match(x)
			if m is not None:
				inputx = Input()
				inputx.name = m.group(1)
				inputlist.append(inputx)
			else:
				p = re.compile("\s*output\s*(\S*);")
				m = p.match(x)
				if m is not None:
					outputx = Output()
					outputx.name = m.group(1)
					outputlist.append(outputx)

	

	#put cursor at begining of file		
	verilogfile.close()
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")

	#get buses
	for x in verilogfile:
		p = re.compile("\s*wire\s*\[(\d+):\d\]\s*(\S+)\s*;")
		m = p.match(x)
		if m is not None:
			for i in range(int(m.group(1))+1):
				wirex = Wire()
				wirex.name = m.group(2)+" ["+str(i)+"]"
				wirelist.append(wirex)
		else:
			p = re.compile("\s*input\s*\[(\d+):\d\]\s*(\S+)\s*;")
			m = p.match(x)
			if m is not None:
				for i in range(int(m.group(1))+1):
					inputx = Input()
					inputx.name = m.group(2)+" ["+str(i)+"]"
					inputlist.append(inputx)
			else:
				p = re.compile("\s*output\s*\[(\d+):\d\]\s*(\S+)\s*;")
				m = p.match(x)
				if m is not None:
					for i in range(int(m.group(1))+1):
						outputx = Output()
						outputx.name = m.group(2)+" ["+str(i)+"]"
						outputlist.append(outputx)
	########output wire names
	i = 0 
	for j in wirelist:
		#print (wirelist[i].name)
		i = i+1
	i = 0 
	for j in inputlist:
		print (inputlist[i].name)
		i = i+1
	i = 0 
	for j in outputlist:
		print (outputlist[i].name)
		i = i+1
	###########################
	
	#put cursor at begining of file		
	verilogfile.close()
	verilogfile = open(filePath)
	if (verilogfile.closed):
		print ("File failed to Open")
	else:
		print ("File Open")

	#get gates
	gatelist = []
	k = 0
	for x in verilogfile:
		p = re.compile("\s*INVX1\s*(\S+)\s*\(\s*")
		m = p.match(x)
		if m is not None:
			gatelist.append(Gate())
			gatelist[k].gtype = "INVX1"
			gatelist[k].name = m.group(1)
			j = verilogfile.readline()
			p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
			m = p.match(j)
			gatelist[k].inputport1 = m.group(1)
			j = verilogfile.readline()
			p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
			m = p.match(j)
			gatelist[k].outputport = (m.group(1))
			k = k+1
		else:
			p = re.compile("\s*NOR2X1\s*(\S+)\s*\(\s*")
			m = p.match(x)
			if m is not None:
				gatelist.append(Gate())
				gatelist[k].gtype = "NOR2X1"
				gatelist[k].name = m.group(1)
				j = verilogfile.readline()
				p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
				m = p.match(j)
				gatelist[k].inputport1 = m.group(1)
				j = verilogfile.readline()
				p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
				m = p.match(j)
				gatelist[k].inputport2 = m.group(1)
				j = verilogfile.readline()
				p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
				m = p.match(j)
				gatelist[k].outputport = (m.group(1))
				k = k+1
			else:
				p = re.compile("\s*XOR2X1\s*(\S+)\s*\(\s*")
				m = p.match(x)
				if m is not None:
					gatelist.append(Gate())
					gatelist[k].gtype = "XOR2X1"
					gatelist[k].name = m.group(1)
					j = verilogfile.readline()
					p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
					m = p.match(j)
					gatelist[k].inputport1 = m.group(1)
					j = verilogfile.readline()
					p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
					m = p.match(j)
					gatelist[k].inputport2 = m.group(1)
					j = verilogfile.readline()
					p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
					m = p.match(j)
					gatelist[k].outputport = (m.group(1))
					k = k+1
				else:
					p = re.compile("\s*XNOR2X1\s*(\S+)\s*\(\s*")
					m = p.match(x)
					if m is not None:
						gatelist.append(Gate())
						gatelist[k].gtype = "XNOR2X1"
						gatelist[k].name = m.group(1)
						j = verilogfile.readline()
						p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
						m = p.match(j)
						gatelist[k].inputport1 = m.group(1)
						j = verilogfile.readline()
						p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
						m = p.match(j)
						gatelist[k].inputport2 = m.group(1)
						j = verilogfile.readline()
						p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
						m = p.match(j)
						gatelist[k].outputport = (m.group(1))
						k = k+1
					else:
						p = re.compile("\s*NAND2X1\s*(\S+)\s*\(\s*")
						m = p.match(x)
						if m is not None:
							gatelist.append(Gate())
							gatelist[k].gtype = "NAND2X1"
							gatelist[k].name = m.group(1)
							j = verilogfile.readline()
							p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
							m = p.match(j)
							gatelist[k].inputport1 = m.group(1)
							j = verilogfile.readline()
							p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
							m = p.match(j)
							gatelist[k].inputport2 = m.group(1)
							j = verilogfile.readline()
							p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
							m = p.match(j)
							gatelist[k].outputport = (m.group(1))
							k = k+1
						else:
							p = re.compile("\s*AND2X2\s*(\S+)\s*\(\s*")
							m = p.match(x)
							if m is not None:
								gatelist.append(Gate())
								gatelist[k].gtype = "AND2X2"
								gatelist[k].name = m.group(1)
								j = verilogfile.readline()
								p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
								m = p.match(j)
								gatelist[k].inputport1 = m.group(1)
								j = verilogfile.readline()
								p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
								m = p.match(j)
								gatelist[k].inputport2 = m.group(1)
								j = verilogfile.readline()
								p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
								m = p.match(j)
								gatelist[k].outputport = (m.group(1))
								k = k+1
							else:
								p = re.compile("\s*OR2X2\s*(\S+)\s*\(\s*")
								m = p.match(x)
								if m is not None:
									gatelist.append(Gate())
									gatelist[k].gtype = "OR2X2"
									gatelist[k].name = m.group(1)
									j = verilogfile.readline()
									p = re.compile("\s*\.A\((\S+\s*\S*)\),\s*")
									m = p.match(j)
									gatelist[k].inputport1 = m.group(1)
									j = verilogfile.readline()
									p = re.compile("\s*\.B\((\S+\s*\S*)\),\s*")
									m = p.match(j)
									gatelist[k].inputport2 = m.group(1)
									j = verilogfile.readline()
									p = re.compile("\s*\.Y\((\S+\s*\S*)\)\s*")
									m = p.match(j)
									gatelist[k].outputport = (m.group(1))
									k = k+1
								else:
									p = re.compile("\s*DFFPOSX1\s*(\S+)\s*\(\s*")
									m = p.match(x)
									if m is not None:
										gatelist.append(Gate())
										gatelist[k].gtype = "DFFPOSX1"
										gatelist[k].name = m.group(1)
										j = verilogfile.readline()
										p = re.compile("\s*\.CLK\((\S+\s*\S*)\),\s*")
										m = p.match(j)
										gatelist[k].inputport1 = m.group(1)
										j = verilogfile.readline()
										p = re.compile("\s*\.D\((\S+\s*\S*)\),\s*")
										m = p.match(j)
										gatelist[k].inputport2 = m.group(1)
										j = verilogfile.readline()
										p = re.compile("\s*\.Q\((\S+\s*\S*)\)\s*")
										m = p.match(j)
										gatelist[k].outputport = (m.group(1))
										k = k+1

	h = 0 
	for z in gatelist:
		#print(gatelist[h].gtype+" "+gatelist[h].name+" "+gatelist[h].inputport1+" "+gatelist[h].inputport2+" "+gatelist[h].outputport)
		h = h+1




if __name__ == "__main__":
	main()