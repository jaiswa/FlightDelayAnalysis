import numpy as np 
import pandas as pd 
from numpy.random import normal
import operator

flights = pd.read_csv('flights.csv')
airports = pd.read_csv('airports.csv')
flights['flight_count'] =1
flights['delay_count'] =5
feature_set ={}
## Extracting features for each airport
for index, row in airports.iterrows():
    Temp = flights[(flights['ORIGIN_AIRPORT'] == row['IATA_CODE'])]
    k = Temp.T.apply(lambda x: x.nunique(), axis=1)
    FlightCount_perday = Temp.groupby(['MONTH','DAY','DAY_OF_WEEK'],as_index = False)['flight_count'].sum() 
    Winter_Data = Temp[(Temp['MONTH'] == 12)]
   
    Weekend_Data = Temp[(Temp['DAY_OF_WEEK'] == 4)]
    FlightsDeparture_everyhour = Temp.groupby(['MONTH','DAY','DAY_OF_WEEK','SCHEDULED_DEPARTURE'],as_index = False)['flight_count'].sum() 
    FlightsDeparture_eachday  =  FlightsDeparture_everyhour.groupby(['MONTH','DAY','DAY_OF_WEEK'],as_index = False)['flight_count'].sum()
    FlightsArrival_everyhour = Temp.groupby(['MONTH','DAY','DAY_OF_WEEK','SCHEDULED_ARRIVAL'],as_index = False)['flight_count'].sum() 
    FlightsArrival_eachday  =  FlightsArrival_everyhour.groupby(['MONTH','DAY','DAY_OF_WEEK'],as_index = False)['flight_count'].sum()
    c = FlightsDeparture_eachday['flight_count'].mean() - FlightsArrival_eachday['flight_count'].mean()
    Temp.SCHEDULED_DEPARTURE = (Temp.SCHEDULED_DEPARTURE - (Temp.SCHEDULED_DEPARTURE%100))/100
    Temp.delay_count[Temp.DEPARTURE_DELAY > 15] = 1 
    Temp.delay_count[Temp.DEPARTURE_DELAY < 15] = 0 
    Temp.delay_count[Temp.DEPARTURE_DELAY == 15] = 1 
    Evening_Data = Temp[(Temp['SCHEDULED_DEPARTURE'] == 24)]   
    
    feature_1=Temp['DEPARTURE_DELAY'].mean()
    feature_2=Temp['ARRIVAL_DELAY'].mean()
    feature_3=Temp['TAXI_OUT'].mean()
    feature_4=Temp['TAXI_IN'].mean()
    feature_5=Temp['WHEELS_OFF'].mean()  
    feature_6=Temp['WHEELS_ON'].mean()    
    feature_7=Temp['DISTANCE'].mean()#distance
    feature_8=Winter_Data['DEPARTURE_DELAY'].mean()#avg departure delay in winter
    feature_9=Winter_Data['ARRIVAL_DELAY'].mean()#avg arrival delay in winter
    feature_10= FlightCount_perday['flight_count'].mean() #no. of flights per day
    feature_11=Weekend_Data['DEPARTURE_DELAY'].mean()#avg departure delay in weekend
    feature_12=Weekend_Data['ARRIVAL_DELAY'].mean()#avg arrival delay in weekend
    feature_13= k['DESTINATION_AIRPORT'] #no. of connecting airports
    feature_14 = k['AIRLINE']#no. of airline from one airport
    feature_15 = c #air traffic
    feature_16 = Temp['delay_count'].mean() #probability of delay of a scheduled flight
    feature_17 = Temp['CANCELLED'].mean() #probability of cancellation
    feature_18 =Evening_Data['DEPARTURE_DELAY'].mean()#avg delay in night time due to accumulation
    feature_set[row['IATA_CODE']] = [feature_1,feature_2,feature_3,feature_4,feature_5,
                        feature_6,feature_7,feature_8,feature_9,feature_10,feature_11,feature_12,feature_13,feature_14,feature_15,
                        feature_16,feature_17,feature_18]
weight_vector = [-1,-1,1,1,-1,-1,2,-2,-2,2,-1,-1,2,2,-1,-3,-3,-1] #weight vector corresponding to features in order

#generating score 
for key in feature_set:
    feature_set[key] = temp_x = np.multiply(feature_set[key],weight_vector)
    feature_set[key] = feature_set[key][~np.isnan(feature_set[key])]
    feature_set[key] = (sum(feature_set[key]))
#Sorting on the basis of score and ranking
Ranked = (sorted(feature_set.items(),reverse=True, key=operator.itemgetter(1))) 
Ranked_Airport = pd.DataFrame(columns=['IATA_CODE', 'score'])
for item in Ranked:
    Ranked_Airport = Ranked_Airport.append(pd.Series([item[0], item[1]], index=['IATA_CODE', 'score']), ignore_index=True)

#naming the airports
airports_dict = dict(zip(airports['IATA_CODE'],airports['AIRPORT']))
Ranked_Airport['AIPORT_desc'] = Ranked_Airport['IATA_CODE'].apply(lambda a: airports_dict[a])

Ranked_Airport.to_csv('ranked_airport.csv')   


    
