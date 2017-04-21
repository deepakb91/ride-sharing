import Trips

minutes = int(raw_input("Window size (min) to run this algorithm:  "))
seconds = minutes*60
Trips.get_all(seconds)


