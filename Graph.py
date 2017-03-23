import networkx as nx

def create_graph(tripList):
	print "Creating graph..."
	merged_trip = {}
	for i in range(len(tripList)):
		trip_set = tripList[i]
		for j in range(len(trip_set)):
				G=nx.Graph()
				G.add_node(trip_set[j].trip_id)
				for k in range(i+1,len(trip_set)):

			print str(trip.trip_id) + " - " + str(trip.trip_distance)
