import networkx as nx

def main():

def practicingNodes():
	G=nx.DiGraph()
	G.add_node(1)
	G.add_nodes_from([2, 3])

	H=nx.path_graph(10) #this adds nbunch of nodes
	print(H.edges())
	G.add_nodes_from(H) #this adds the nodes contained in H to G
	G.add_node(H) #this however adds H as a node.
	print(G.nodes()) #print all nodes that exist in graph G
	G.add_edge(1, 2) #add edge between node 1 and 2
	e=(2, 3)
	G.add_edge(*e)
	G.add_edges_from([(1, 2), (1, 3)])
	G.add_edges_from(H.edges()) #add edges from graph H
	print(G.edges())
	G.remove_node(H) #remove
	print(G.number_of_nodes())
	G[1]['gInfo'] = 'xor' 
	print(G[1])

#myGraph is a graph, gInp is other gates to
def addGate(myGraph, ID, gType, gInp):
	myGraph.add_node(ID) #create a new gate with unique ID that is determined outside of this method
	myGraph[ID]['gate']=gType #specify the gate type i.e 'xor'

	#this loop not tested yet
	for i in gInp: #connect this gate with other gates thus creating edges or inputs
		myGraph.add_edge(i, ID)


if __name__ == "__main__":
  main()
