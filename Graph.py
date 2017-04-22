import networkx as nx
import GraphHopperUtils
import math
def create_graph(tripList):
	print "Merging..."
	merged_history = {}
	merged_trip_id_list = []
	merged_trip_list = []
	total_trips = 0
	#for i in range(len(tripList)):
	for i in range(1):
		trip_set = tripList[i]
		total_trips+=len(trip_set)
		merged_trip_id_set = []
		merged_trip_set = []
		for j in range(len(trip_set)):
			merged_trip_id = []
			merged_trip = []
			shouldAppend = False 
			#print "Checking for trip - " + str(j+1) 
			if trip_set[j].trip_id not in merged_history:
				first_add = True
				trip_id = 0
				existing_passengers = trip_set[j].passengers
				previous_trip = trip_set[j]
				previous_trip_id = trip_set[j].trip_id
				isContinue = True
				while existing_passengers < 4 and isContinue == True:
					gain = 0.0
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
						shouldAppend = True
						if first_add == True:
							merged_history[previous_trip_id] = previous_trip_id
							merged_trip_id.append(previous_trip_id)
							merged_trip.append(previous_trip)
							first_add = False
						merged_history[trip_id] = trip_id
						previous_trip = trip
						previous_trip_id = 	trip_id
						merged_trip_id.append(trip_id)
						merged_trip.append(trip)
						existing_passengers = existing_passengers + trip.passengers
					else:
						isContinue = False				
			if shouldAppend == True: 
				merged_trip_id_set.append(merged_trip_id)
				merged_trip_set.append(merged_trip)		
		merged_trip_id_list.append(merged_trip_id_set)
		merged_trip_list.append(merged_trip_set)
	merged_trips_count=0
	lone_trips_count = 0
	for trip_set in merged_trip_id_list:
		merged_trips_count+=len(trip_set)
	total_original_distance = 0;
	#for i in range(len(tripList)):
	for i in range(1):
		for trips in tripList[i]:
			total_original_distance+=trips.distance
			if trips.trip_id not in merged_history:
				lone_trips_count+=1				
	print "Now we have " + str(merged_trips_count + lone_trips_count) + " trips after merging."
	print str(lone_trips_count) + " trips are unmerged"
	print "Calculating cost saved..."
	print str(total_original_distance) + " miles was travelled by the taxis before merging"
	total_original_cost = total_original_distance + (total_trips * 0.25)
	print "Total original cost: $" + str(total_original_cost)
	estimate_cost_saved(merged_trip_list)
	
def distance_gain(first_trip,second_trip):
	result = GraphHopperUtils.distance_for_multiple_destinations(40.644104, -73.782665, first_trip.dropoff_latitude,first_trip.dropoff_longitude,second_trip.dropoff_latitude,second_trip.dropoff_longitude)
	first_distance = first_trip.distance
	second_distance = second_trip.distance
	new_distance = result[0]
	gain = float((first_distance + second_distance - new_distance)/(first_distance + second_distance))
	return gain

def estimate_cost_saved(merged_trip_list):
	total_merged_trip_cost = 0
	total_merged_trip_distance = 0
	for merged_trip_set in merged_trip_list:
		for trips in merged_trip_set:
			merged_trip_cost = 0
			total_individual_distance = 0
			coordinates = (40.644104, -73.782665)
			for trip in trips:
				total_individual_distance+=trip.distance
				coordinates = coordinates + (trip.dropoff_latitude,trip.dropoff_longitude) 
			result = GraphHopperUtils.distance_from_jfk(coordinates)
			merged_trip_distance = result[0]
			total_merged_trip_distance+=merged_trip_distance
			fraction = merged_trip_distance/total_individual_distance
			for trip in trips:
				merged_trip_cost+=(fraction*trip.distance) + 0.5
			total_merged_trip_cost+=merged_trip_cost
	print "After merging, the taxis will have to travel " + str(total_merged_trip_distance) + " miles."			
	print "Total cost after merging :$" + str(total_merged_trip_cost)
