import pandas as pd

# load gtfs data
stops = pd.read_csv("raw_data/stops.txt")
trips = pd.read_csv("raw_data/trips.txt")
stop_times = pd.read_csv("raw_data/stop_times.txt")
routes = pd.read_csv("raw_data/routes.txt")
calendar = pd.read_csv("raw_data/calendar.txt")

'''DEBUGGING:
print("\nSTOPS\n", stops.head())
print("\n\nTRIPS\n", trips.head())
print("\n\nSTOP TIMES\n", stop_times.head())
print("\n\nROUTES\n", stop_times.head())
print("\n\nCALENDAR\n", stop_times.head(), "\n\n\n")
#'''

# filter for F/M lines weekday stop times
fm_trips = trips[trips['route_id'].isin(['F', 'M'])]
weekday_fm_trips = fm_trips[fm_trips['service_id']=="Weekday"]
weekday_stop_times = stop_times.merge(weekday_fm_trips[['trip_id', 'route_id', 'direction_id', 'service_id']], on='trip_id', how='inner').drop_duplicates().sort_values(['trip_id', 'stop_sequence'])

'''DEBUGGING:
print("\nFiltered for F/M Lines")
print("\n\nTRIPS\n", fm_trips.head())
print("\n\nWEEKDAY TRIPS\n", weekday_fm_trips.head())
print("\n\nWEEKDAYSTOP TIMES\n", weekday_stop_times.head(), "\n\n\n")
#'''

# make consecutive stop pairs
edges = []
for trip_id, group in weekday_stop_times.groupby('trip_id'):
    stops_in_trip = group[['stop_id', 'departure_time', 'stop_sequence']].sort_values('stop_sequence')
    cleaned_stops = stops_in_trip[['stop_id', 'departure_time']].drop_duplicates().values
    
    '''DEBUGGING:
    print("\nTrip: ", trip_id)
    print("\n\nSTOPS\n", stops_in_trip)
    print("\n\nCLEANED\n", cleaned_stops, "\n\n\n")
    break
    #'''

    for i in range(len(cleaned_stops)-1):
        src, dep_time = cleaned_stops[i]
        dst, arr_time = cleaned_stops[i+1]
        travel_time = pd.to_timedelta(arr_time) - pd.to_timedelta(dep_time)
        edges.append({
            'trip_id': trip_id,
            'src': src,
            'dst': dst,
            'travel_time_sec': travel_time.total_seconds()
        })

        '''DEBUGGING:
        print("\nTrip: ", trip_id)
        print("INDEX: ", i)
        print("SOURCE: ", src)
        print("DESTINATION: ", dst)
        print("TRAVEL TIME (s): ", travel_time.total_seconds(), "\n")
    break
    #'''

edges_df = pd.DataFrame(edges)
'''
print("\nEDGES\n", edges_df.head())
'''