import json
from urllib2 import URLError, Request, urlopen

def get_time_in_minutes(milliseconds):
    minutes, reminder = divmod(milliseconds, 60000)
    if reminder >= 50:
        minutes += 1
    return minutes

def meters_to_miles(meters):
    miles = meters / 1609.344
    return round(miles, 2)

def distance_for_a_destination(source_latitude, source_longitude, destination_latitude, destination_longitude):
    source = str(source_latitude) + ',' + str(source_longitude)
    destination = str(destination_latitude) + ',' + str(destination_longitude)
    request_string = "http://localhost:8989/route?point=" + source + "&point=" + destination
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meters_to_miles(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except URLError:
        result = [-1, -1]
    return result

def distance_for_multiple_destinations(source_latitude, source_longitude, destination_latitude, destination_longitude, destination_latitude1, destination_longitude1):
    source = str(source_latitude) + ',' + str(source_longitude)
    destination = str(destination_latitude) + ',' + str(destination_longitude)
    destination1 = str(destination_latitude1) + ',' + str(destination_longitude1)
    request_string = "http://localhost:8989/route?point=" + source + "&point=" + destination + "&point=" + destination1
    print request_string
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meters_to_miles(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except URLError:
        result = [-1, -1]
    return result
