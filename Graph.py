import networkx as nx
import GraphHopperUtils

def create_graph(tripList):
	print "Merging..."
	merged_history = {}
	merged_trip_list=[]
	lone_trip_list=[]
	#for i in range(len(tripList)):
	for i in range(1):
		#print "First"
		trip_set = tripList[i]
		merged_trip_set = []
		for j in range(len(trip_set)):
			#print "Second" + str(j)
			#G=nx.Graph()
			#G.add_node(trip_set[j].trip_id)
			if trip_set[j].trip_id not in merged_history:
				merged_trip = []
				first_add = True
				gain = 0.0
				trip_id = 0
				existing_passengers = trip_set[j].passengers
				previous_trip = trip_set[j]
				previous_trip_id = trip_set[j].trip_id
				isContinue = True 
				while existing_passengers < 4 and isContinue ==True:
					#print "While"
					for k in range(len(trip_set)):
						#print "Third" + str(k)
						if trip_set[k].trip_id not in merged_history and trip_set[k].trip_id != previous_trip_id:
							if (existing_passengers + trip_set[k].passengers) > 4:
								pass
							else:
								new_gain = distance_gain(trip_set[j],trip_set[k])
								if new_gain > gain:
									gain=new_gain
									trip = trip_set[k]
									trip_id = trip.trip_id
						if k == len(trip_set) -1:
							isContinue=False			
					if gain != 0.0:
						if first_add == True:
							merged_history[previous_trip_id] = previous_trip_id
							merged_trip.append(previous_trip_id)
							first_add = False
						merged_history[trip_id] = trip_id
						previous_trip = trip
						previous_trip_id = 	trip_id
						merged_trip.append(trip_id)
						existing_passengers = existing_passengers + trip_set[k].passengers			
			merged_trip_set.append(merged_trip)
		#print str(len(trip_set)) + " trips was reduced to " + str(len(merged_trip)) + " trips"			
		merged_trip_list.append(merged_trip_set)		



def distance_gain(first_trip,second_trip):
	result = GraphHopperUtils.distance_for_multiple_destinations(40.644104, -73.782665, first_trip.dropoff_latitude,first_trip.dropoff_longitude,second_trip.dropoff_latitude,second_trip.dropoff_longitude)
	first_distance = first_trip.distance
	second_distance = second_trip.distance
	new_distance = result[0]
	gain = float((first_distance + second_distance - new_distance)/(first_distance + second_distance))
	#print gain
	return gain
