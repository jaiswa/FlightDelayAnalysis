import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from numpy.random import normal

airlines = pd.read_csv('/home/Downloads/flight-delays/airlines.csv')
flights = pd.read_csv('/home/Downloads/flight-delays/flights.csv')
month_dict={
    1:  'January',
    2:  'February',
    3:  'March',
    4:  'April',
    5:  'May',
    6:  'June',
    7:  'July',
    8:  'August',
    9:  'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

airlines_dict = dict(zip(airlines['IATA_CODE'],airlines['AIRLINE']))
flights['AIRLINE_desc'] = flights['AIRLINE'].apply(lambda a: airlines_dict[a])
flights['MONTH_desc'] = flights['MONTH'].apply(lambda m: month_dict[m])



def vis_by_airport( mylist ):
    Index =[0,1,2,3]
    Airport_code = ['CAE','CLD','JFK','LAX']
    Airport_name = ['Columbia','San Digo','New York','Los Angeles']
    airport  = {}
    mylist[3], axarr = plt.subplots(4, sharex=True)
    axarr[0].set_title(mylist[0])
    for i,code,name in zip(Index,Airport_code,Airport_name):
        Temp = flights[(flights['ORIGIN_AIRPORT'] == code)]
        airport[code] = Temp.groupby([mylist[1]],as_index = False)[mylist[2]].mean()
        axarr[i].set_ylabel(name)
        airport[code].plot(x=mylist[1],y=mylist[2],kind ='bar',ax = axarr[i])
        mylist[3].tight_layout()

def vis_over_whole_data(mylist):
    Temp = flights.groupby(mylist[1], as_index=False)[mylist[2]].mean()
    fig = plt.figure(mylist[3])
    Temp.plot(x=mylist[1],y=mylist[2],kind ='bar')
    plt.title(mylist[0])
    plt.ylabel(mylist[4])
    fig.tight_layout()
    fig.show()
        
def dep_delay_distribution(mylist):
    f13 = plt.figure(13)
    plt.hist(flights.DEPARTURE_DELAY.dropna(),range=[-30, 150] ,bins=60, normed=True)
    plt.title("Departure DELAY DISTRIBUTION")
    plt.xlabel("min")
    plt.ylabel("probability")
    f13.show()
    
def arr_delay_distribution(mylist):
    f14 = plt.figure(14)
    plt.hist(flights.ARRIVAL_DELAY.dropna(),range=[-30, 150] ,bins=60, normed=True)
    plt.title("Arrival DELAY DISTRIBUTION")
    plt.xlabel("min")
    plt.ylabel("probability")        
    f14.show()    
        
        
        
print "Select The Index of the given option you want to visualize:"
print "1:Average Departure Delay by month for four Airports"
print "2:Average Arrival Delay by month for four Airports" 
print "3:Average Departure Delay by Carrier for four Airports"
print "4:Average Arrival Delay by Carrier for four Airports"
print "5:Average Departure Delay by Time of Day for four Airports"
print "6:Average Arrival Delay by Time of Day for four Airports"
print "7:Probability of cancelling the flight by month for four Airports"
print "8:Average Departure Delay by Month"
print "9:Average Arrival Delay by Month"
print "10:Average Departure Delay by Carrier"
print "11:Average Arrival Delay by Carrier"
print "12:probability of cancelled flight month wise"
print "13:Departure delay distribution over whole data"
print "14:Arrival delay distribution over whole data"

plot_no = input()


if plot_no == 1:
   mylist =  ['Average Departure Delay by month for four Airports','MONTH_desc','DEPARTURE_DELAY',1]
   vis_by_airport( mylist );
   mylist[3].show()
elif plot_no == 2:
    mylist = ['Average Arrival Delay by month for four Airports','MONTH_desc','ARRIVAL_DELAY',2]
    vis_by_airport( mylist );
    mylist[3].show()
elif plot_no == 3:
    mylist = ['Average Arrival Delay by Carrier for four Airports','AIRLINE_desc','DEPARTURE_DELAY',3]
    vis_by_airport( mylist );
    mylist[3].show()
elif plot_no == 4:
    mylist = ['Average Arrival Delay by Carrier for four Airports','AIRLINE_desc','ARRIVAL_DELAY',4]
    vis_by_airport( mylist );
    mylist[3].show()
elif plot_no == 5:
    flights.SCHEDULED_DEPARTURE = (flights.SCHEDULED_DEPARTURE - (flights.SCHEDULED_DEPARTURE%100))/100
    mylist = ['Average Departure Delay by Time of Day for four Airports','SCHEDULED_DEPARTURE','DEPARTURE_DELAY',5]
    vis_by_airport( mylist );
    mylist[3].show()
elif plot_no == 6:
    flights.SCHEDULED_ARRIVAL = (flights.SCHEDULED_ARRIVAL - (flights.SCHEDULED_ARRIVAL%100))/100
    mylist = ['Average Arrival Delay by Time of Day for four Airports','SCHEDULED_ARRIVAL','ARRIVAL_DELAY',6]
    vis_by_airport( mylist );
    mylist[3].show()
elif plot_no == 7:
    mylist = ['Probability of cancelling the flight by month for four Airports','MONTH_desc','CANCELLED',7]
    vis_by_airport( mylist );
    mylist[3].show()

elif plot_no == 8:
    mylist = ['Average Departure Delay by Month','MONTH_desc','DEPARTURE_DELAY',8,'Departure Delay in min']
    vis_over_whole_data( mylist );
elif plot_no == 9:
    mylist = ['Average Arrival Delay by Month','MONTH_desc','ARRIVAL_DELAY',9,'ARRIVAL Delay in min']
    vis_over_whole_data( mylist );       
    
elif plot_no == 10:
    mylist = ['Average Departure Delay by Carrier','AIRLINE','DEPARTURE_DELAY',10,'Departure Delay in min']
    vis_over_whole_data( mylist );
elif plot_no == 11:
    mylist = ['Average Arrival Delay by Carrier','AIRLINE','ARRIVAL_DELAY',11,'ARRIVAL Delay in min']
    vis_over_whole_data( mylist ); 
elif plot_no == 12:
    mylist = ['Probability of cancelled flight month wise','MONTH_desc','CANCELLED',12,'Prob of cancellation']
    vis_over_whole_data( mylist ); 
    
elif plot_no == 13:
    mylist = [13]
    dep_delay_distribution( mylist ); 
elif plot_no == 14:
    mylist = [14]
    arr_delay_distribution( mylist ); 
