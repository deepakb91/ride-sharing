import networkx as nx
import GraphHopperUtils

def create_graph(tripList):
	print "Merging..."
	merged_history = {}
	merged_trip_list=[]
	lone_trip_list=[]
	total_trips = 0
	#for i in range(len(tripList)):
	for i in range(2):
		trip_set = tripList[i]
		total_trips+=len(trip_set)
		merged_trip_set = []
		for j in range(len(trip_set)):
			merged_trip = []
			shouldAppend = False 
			#print "Checking for trip - " + str(j+1) 
			if trip_set[j].trip_id not in merged_history:
				first_add = True
				gain = 0.0
				trip_id = 0
				existing_passengers = trip_set[j].passengers
				previous_trip = trip_set[j]
				previous_trip_id = trip_set[j].trip_id
				isContinue = True
				while existing_passengers < 4 and isContinue == True:
					for k in range(len(trip_set)):
						if (trip_set[k].trip_id not in merged_history) and (trip_set[k].trip_id != previous_trip_id):
							if (existing_passengers + trip_set[k].passengers) > 4:
								pass
							else:
								new_gain = distance_gain(previous_trip,trip_set[k])
								if new_gain > gain:
									gain=new_gain
									trip = trip_set[k]
									trip_id = trip.trip_id							
					if gain != 0.0:
						print "Previous - " + str(previous_trip_id) + " Current - " + str(trip_id)
						print (trip_id not in merged_history)
						print trip_id != previous_trip_id
						shouldAppend = True
						if first_add == True:
							merged_history[previous_trip_id] = previous_trip_id
							merged_trip.append(previous_trip_id)
							first_add = False
						merged_history[trip_id] = trip_id
						previous_trip = trip
						previous_trip_id = 	trip_id
						merged_trip.append(trip_id)
						existing_passengers = existing_passengers + trip.passengers
					else:
						isContinue = False				
			if shouldAppend == True:
				print merged_trip 
				merged_trip_set.append(merged_trip)		
		merged_trip_list.append(merged_trip_set)

	merged_trips_count=0
	for trip_set in merged_trip_list:
		merged_trips_count+=len(trip_set)

	
	print "Now we have " + str(merged_trips_count) + " trips after merging."
	'''
	print "------------"
	for trip_set in merged_trip_list:
		for merged_trips in trip_set:
			print merged_trips
	''' 	


def distance_gain(first_trip,second_trip):
	result = GraphHopperUtils.distance_for_multiple_destinations(40.644104, -73.782665, first_trip.dropoff_latitude,first_trip.dropoff_longitude,second_trip.dropoff_latitude,second_trip.dropoff_longitude)
	first_distance = first_trip.distance
	second_distance = second_trip.distance
	new_distance = result[0]
	gain = float((first_distance + second_distance - new_distance)/(first_distance + second_distance))
	#print gain
	return gain
