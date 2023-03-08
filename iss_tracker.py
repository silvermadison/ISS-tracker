import requests
import xmltodict
import math
import time
from geopy.geocoders import Nominatim
from flask import Flask
from flask import request

app = Flask(__name__)

url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"
response = requests.get(url)
info = xmltodict.parse(response.text)
data = info['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods = ['GET'])
def get_data_set():
    '''
        This function gets the entire ISS data set that we are using

        Returns:
        data (dict): a dictionary of usable ISS data with the same keys
    '''
    return data

@app.route('/epochs', methods = ['GET']) #/epochs?limit=int&offset=int 
def epoch_args():
    '''
        This function returns only a list of epochs which is a key name.

        Returns:
            epoch_list(list): a list of epoch data between offset (a start parameter) and limit (the ending parameter)
    '''
    maximum = len(data)
    epoch_list = []
    limit = request.args.get('limit', maximum)
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return "Invalid limit parameter; limit must be an integer.", 400
    offset = request.args.get('offset', 0) #start
    if offset:
        try:
            offset = int(offset)
        except ValueError:
            return "Invalid offset parameter; offset must be an integer.", 400
    count=limit
    for i in range(maximum):
        if len(epoch_list)==limit:
            break
        if i>=offset:
            epoch_list.append(data[i]['EPOCH'])
    return epoch_list

@app.route('/epochs/<int:epoch>', methods = ['GET'])
def get_an_epoch_data(epoch):
    '''
        This function finds the data of a specific epoch/data set.

        Args:
            epoch (int): the specific number of the data set to look at

        Returns:
            data[epoch] (dict): a dictionary of the specific data set requested with unique keys about its position and velocity data
    '''
    if epoch>=len(data):
        return "Error: Epoch value is not in the data set" , 400
    return data[epoch]

@app.route('/epochs/<int:epoch>/speed', methods = ['GET'])
def get_speed(epoch):
    '''
        This function finds the speed of a given epoch.

        Args:
            epoch (int): the specific number of the data set to look at

        Returns:
            speed (float): the instantaneous speed of the given epoch
    '''
    speed_data = {}
    #if epoch is not in data - same format as in get_an_epoch_data function
    if epoch>=len(data):
        return "Error: Epoch value is not in the data set", 400
    #use speed eq
    xdot = data[epoch]['X_DOT']['#text']
    ydot = data[epoch]['Y_DOT']['#text']
    zdot = data[epoch]['Z_DOT']['#text']
    xdot = float(xdot)
    ydot = float(ydot)
    zdot = float(zdot)
    calc = (xdot*xdot)+(ydot*ydot)+(zdot*zdot)
    speed = math.sqrt(calc )
    units = data[epoch]['X_DOT']['@units']
    #put data into dict
    speed_data["value"] = speed
    speed_data["units"] = units
    #return (f'speed: {str(speed)} {units}')
    return speed_data

@app.route('/help', methods = ['GET'])
def help():
    '''
        This function contains available routes and a short description of what each returns.
    
        Returns:
            (str): a string with routes and what they return
    '''
    welcome = "Welcome to Help! Below are available routes and their return statements. \n \n"
    r1 = ("The route '/' returns the entire data set. \n") 
    r2 = ("The route '/epochs' returns a list of all the epochs in the data set. \n") 
    r3= ("The route '/epochs?limit=int&offset=int' returns a list of epochs in the data set between offset and limit. If offset is not given then the list will start at the first epoch and if limit is not given the list will end at the last epoch. \n")
    r4 =("The route '/epochs/<epoch>' returns a dictionary of the specific epoch data set requested with unique keys about its position and velocity data. \n")
    r5 = ("The route '/epochs/<epoch>/speed' returns the instantaneous speed for a specific epoch in the data set. \n")
    r6 =("The route '/delete-data' deletes all data from the data set. \n")
    r7 =("The route '/post-data' reloads the dictionary with data from the web. \n")
    r8 = ("The route '/comment' returns a 'comment' list object from ISS data. \n")
    r9 = ("The route '/header' returns a 'header' dict object from ISS data. \n")
    r10 = ("The route '/metadata' returns a 'metadata' dict object from ISS data. \n")
    r11 = ("The route '/epochs/<epoch>/location' returns latitude, longitude, altitude, and geoposition data for a given epoch. \n")
    r12 = ("The route '/now' returns latitude, longitude, altitude, and geoposition data for an epoch that is nearest in time. \n")
    return welcome +r1 + r2 +r3 +r4 +r5 +r6+r7+r8+r9+r10+r11+r12


@app.route('/delete-data', methods = ['DELETE'])
def delete_data():
    '''
        Deletes all the data in the dictionary object.
    
        Returns:
            data(dict): returns an empty dictionary.
    '''
    global data
    data = []; 
    return data #check that it returns nothing

@app.route('/post-data', methods = ['POST'])
def post_data():
    '''
        Reloads the dictionary object with data from ISS on the web.

        Returns:
            (str): a string stating the data has been posted back into the dictionary object holding the data.
    '''
    global data 
    data = info['ndm']['oem']['body']['segment']['data']['stateVector']
    return "the data has been posted \n"

@app.route('/comment', methods = ['GET'])
def comment():
	'''
	    This function returns comments about the ISS.

	    Returns:
		comment(list): a list of specific data about the ISS like its mass, units, drag area, drag coeff, etc.
	'''
	comment = info['ndm']['oem']['body']['segment']['data']['COMMENT']
	return comment

@app.route('/header', methods = ['GET'])
def header():
	'''
    	    This function returns the header of the ISS.

	    Returns:
		header(dict): a dictionary with keys CREATION_DATE and ORIGINATOR providing info about the ISS
	'''
	header = info['ndm']['oem']['header']
	return header

@app.route('/metadata', methods = ['GET'])
def metadata():
	'''
	This function returns the metadata of the ISS.

	Returns:
		metadata(dict): a dictionary of metadata about the ISS
	'''
	metadata = info['ndm']['oem']['body']['segment']['metadata']
	return metadata

@app.route('/epochs/<int:epoch>/location', methods = ['GET'])
def get_location(epoch):
    '''
        This function returns location data for a given epoch.

        Args:
            epoch (int): the specific number of the data set to look at

        Returns:
            location_data (dict): a dictonary with latitude, longitude, altitude, and geolocation data
    '''
    if epoch>=len(data):
        return "Error: Epoch value is not in the data set", 400
    x = data[epoch]['X']['#text']
    y = data[epoch]['Y']['#text']
    z = data[epoch]['Z']['#text']
    x = float(x)
    y = float(y)
    z = float(z)
    units = data[epoch]['Z']['@units']
    mean_earth_radius = 6371000 #meters
    hrs = data[epoch]['EPOCH'][9:11] 
    mins = data[epoch]['EPOCH'][12:14] 
    hrs = int(hrs)
    mins = int(mins)
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))                
    lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
    lon = float(lon)
    if abs(lon) > 180.0: #change sign
        if lon>0:
            lon = lon-180
            lon = 180-lon
        else:
            lon = lon+180
            lon= 180+lon

    alt = math.sqrt(x**2 + y**2 + z**2)-mean_earth_radius
    geocoder = Nominatim(user_agent='iss_tracker')
    geoloc = geocoder.reverse((lat, lon), zoom=15, language='en')
    #create a dictionary for location data
    location_data = {}
    location_data["latitude"] = lat
    location_data["longitude"] = lon
    location_data["altitude"] = {'value':alt , 'units': units}
    if str(geoloc) == "None":
        location_data["geo"] = "geo location is unknown, perhaps it is over the ocean" 
    else: #has a geolocation that is not None
        location_data['geo'] = geoloc.raw['address'] 
    return location_data

@app.route('/now', methods = ['GET'])
def now():
    '''
        This fucntion finds the closest epoch to the current time and returns information about its speed and location.

        Returns:
            now_data (dict): a dictionary with keys including what the closest epoch is, how far in seconds it is from the current time, location from the get_location function, and speed from the get_speed function
    '''
    time_now = time.time()  # gives present time in seconds since unix epoch
    epochs = epoch_args()
    time_epoch = time.mktime(time.strptime(epochs[0][:-5], '%Y-%jT%H:%M:%S'))
    minimum = time_now - time_epoch
    count = 0
    for epoch in epochs:
        time_epoch = time.mktime(time.strptime(epoch[:-5], '%Y-%jT%H:%M:%S'))#epoch in seconds 
        difference = time_now - time_epoch #this includes date too
        if abs(difference) < abs(minimum):
            minimum = difference
            near_epoch = epoch
            epoch_num = count
        count = count+1
    now_location = get_location(epoch_num)
    now_speed = get_speed(epoch_num)
    #create a dictionary of now data
    now_data = {}
    now_data['closest_epoch'] = near_epoch
    now_data['seconds_from_now'] = minimum
    now_data['location'] = now_location
    now_data['speed'] = now_speed 
    return now_data 


#-----------------------------end of routes--------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


