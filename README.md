# International Space Station Tracker
## Objective
The purpose of this project is to track the International Space Station (ISS) by using the ISS's data from its website. This project uses software design principles including REST APIs (Representational State Transfer Application Programming Interfaces), Flask Application, creating routes in Flask using type annotations and docstrings, working with XML data, and containerization with Dockerfiles, Docker Compose, and Docker images. **ADJUST A BIT**

## Contents
This repository includes 1 script, 1 Dockerfile, 1 docker-compose, and 1 README file.

## Required Modules
This project requires the installation of the requests, Flask, xmltodict, and geopy modules. Install these modules with the command ```pip install --user <module>```.

## ISS Data
The International Space Station (ISS) data is a data set of information about the ISS. It is an extremely large dictionary containing metadata, comments about the ISS like units, mass, etc., as well as time, position, and velocity data about where the ISS was, is, and will be in over a 15 day time frame with data points for every 4 minutes. Each data point is a dictionary with keys EPOCH, X, X_DOT, Y, Y_DOT, Z, Z_DOT giving it its unique epoch, position, and velocity data. Within the script file, you can see how robust the data is by viewing how many keys are needed to get to these individual data point dictionaries.

Keeter, Bill. “ISS Trajectory Data.” Edited by Jacob Keaton, Spot the Station International Space Station, NASA, 27 July 2021, https://spotthestation.nasa.gov/trajectory_data.cfm.

### Part 1 - Routes
In the ```iss_tracker.py``` file, it contains instructions for reading the ISS data and the app routes below. The requests and xmltodict modules are used to read the ISS information into a usable dictionary of the data. 

| Route | Method | What it should return | 
| ---------------------------- | ---------------------------- | ---------------------------- |
| ```/``` | GET | the entire data set |
| ```/epochs``` | GET |  a list of all epochs in the set | 
| ```/epochs?limit=int&offset=int``` | GET | a modified list of epochs given query parameters | 
| ```/epochs/<epoch>``` | GET | data for a specific Epoch from the data set |
| ```/epochs/<epoch>/speed``` | GET | instantaneous speed for a specific Epoch in the data set  |
| ```/help``` | GET | a help text (as a string) that briefly describes each route |
| ```/delete-data``` | DELETE | delete all data from the dictionary object |
| ```/post-data``` | POST | reload the dictionary object with data from the web |
| ```/comment``` | GET | return ‘comment’ list object from ISS data |
| ```/header``` | GET | return ‘header’ dict object from ISS data |
| ```/metadata``` | GET | return ‘metadata’ dict object from ISS data |
| ```/epochs/<epoch>/location``` | GET | return latitude, longitude, altitude, and geoposition for a given epoch |
| ```/now``` | GET | return latitude, longitude, altitude, and geoposition data for the epoch that is nearest in time |

In order to find the speed in the ```/epochs/<epoch>/speed``` route the following equation was used:
speed = sqrt(x_dot^2 + y_dot^2 + z_dot^2)


### Part 2 - Dockerfile 
The Dockerfile contains commands for building a new image. When creating the Dockerfile the image should contain the same versions of modules as you are using on the Jetstream VM; this will be reflected in the ```FROM``` and ```RUN``` instructions. We will do this for the modules python, flask, requests, xmltodict, and geopy.

To check your version of python run ```python3``` in the VM command line. Output should look similar to:
```
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
The first line shows you the version of python you are using, in this case I am using Python 3.8.10. This same version is contained in the ```FROM``` instruction in the Dockerfile.

To check your version of flask, in the VM command line run ```pip freeze | grep Flask```. Output should look similar to:
```
Flask==2.2.2
```
The version of Flask I am using is 2.2.2 and this version is also used in the Dockerfile.

To check your version of requests, in the VM command line run ```pip freeze | grep requests```. Output should look similar to:
```
requests==2.22.0
```
The version of requests I am using is 2.22.0 and this version is also used in the ```RUN``` instruction in the Dockerfile.

To check your version of xmltodict, in the VM command line run ```pip freeze | grep xmltodict```. Output should look similar to:
```
xmltodict==0.13.0
```
The version of xmltodict I am using is 0.13.0 and this version is also used in the ```RUN``` instruction in the Dockerfile.
To check your version of geopy, in the VM command line run ```pip freeze | grep geopy```. Output should look similar to:
```
geopy==2.3.0
```
The version of geopy I am using is 2.3.0 and this version is also used in the ```RUN``` instruction in the Dockerfile.


## Instructions
### Cloning the Repository
In order to retrieve the data from this repository use the command ```git clone git@github.com:silvermadison/ISS-tracker.git```.


### Pull the Image from Docker Hub
To get the image from Docker Hub use the command ```docker pull silvermadison/iss_tracker:1.0```.


### Build a New Image from This Dockerfile
Create the image using the command ```docker build -t silvermadison/iss_tracker:1.0 .```. Check to make sure the image is there using the command```docker images```.


### Run the Containerized Flask App
Test the image with the command ```docker run -it --rm silvermadison/iss_tracker:1.0 /bin/bash```.
Once this is run you should be in the container. From here you can go into the python interpreter to ensure the flask, requests, and xmltodict modules have been installed with no errors. This exchange should look like the following:
```
root@9a1f45a8ea52:/# python
Python 3.8.10 (default, Jun 23 2021, 15:19:53) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import flask
>>> import requests
>>> import xmltodict
>>> import geopy
>>> 
```
Quit the python interpreter with ```quit()``` and exit the container. Now we will run Flask using the docker compose file with the command ```docker-compose up```.

### Example Outputs and API Query Commands
Now with the container running, you can test API query commands. In order to run the code, open another tab in your linux operating system so that you have two tabs total. In one tab Flask is running in the foreground and in the other tab API query commands will be made.

The ```/``` route should output the entire ISS dataset:
```
[
  {
    "EPOCH": "2023-048T12:00:00.000Z",
    "X": {
      "#text": "-5097.51711371908",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-4.5815461024513304",
      "@units": "km/s"
    },
    "Y": {
      "#text": "1610.3574036042901",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-4.8951801207083303",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-4194.4848049601396",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "3.70067961081915",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2023-048T12:04:00.000Z",
    "X": {
      "#text": "-5998.4652356788401",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-2.8799691318087701",
      "@units": "km/s"
    },
    "Y": {
      "#text": "391.26194859011099",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-5.2020406581448801",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-3164.26047476555",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "4.8323394499086101",
      "@units": "km/s"
    }
  },
…
]
```

The ```/epochs``` route should output a list of all the epochs in the data set: 
```
[
  "2023-048T12:00:00.000Z",
  "2023-048T12:04:00.000Z",
  "2023-048T12:08:00.000Z",
  "2023-048T12:12:00.000Z",
  "2023-048T12:16:00.000Z",
…
]
```


Some example output for the limit and offset query parameters are below. 

Test the limit parameter with the command ```curl localhost:5000/epochs?limit=10```. The output should be a total of 10 epochs:
```
[
  "2023-055T12:00:00.000Z",
  "2023-055T12:04:00.000Z",
  "2023-055T12:08:00.000Z",
  "2023-055T12:12:00.000Z",
  "2023-055T12:16:00.000Z",
  "2023-055T12:20:00.000Z",
  "2023-055T12:24:00.000Z",
  "2023-055T12:28:00.000Z",
  "2023-055T12:32:00.000Z",
  "2023-055T12:36:00.000Z"
]
```

To use both parameters together you must run the ```curl``` a little differently: ```curl 'localhost:5000/epochs?limit=3&offset=2'```. The output should start the epochs list on the 3rd epoch (offset by 2) and have the next 3 epochs:
```
[
  "2023-055T12:08:00.000Z",
  "2023-055T12:12:00.000Z",
  "2023-055T12:16:00.000Z"
]
```


The ```/epochs/1``` route should output the positional and velocity data for a specific epoch: 
```
{
  "EPOCH": "2023-048T12:04:00.000Z",
  "X": {
    "#text": "-5998.4652356788401",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-2.8799691318087701",
    "@units": "km/s"
  },
  "Y": {
    "#text": "391.26194859011099",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-5.2020406581448801",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-3164.26047476555",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "4.8323394499086101",
    "@units": "km/s"
  }
}
```

The ```/epochs/1/speed``` route should output the instantaneous speed for a specific epoch:
```
speed: 7.662046317290625 km/s
```


For the ```/help``` route the output should be an explanation of all the routes and their outputs:
```
Welcome to Help! Below are available routes and their return statements. 

The route '/' returns the entire data set. 
The route '/epochs' returns a list of all the epochs in the data set.
The route '/epochs?limit=int&offset=int' returns a list of epochs in the data set between offset and limit. If offset is not given then the list will start at the first epoch and if limit is not given the list will end at the last epoch.
The route '/epochs/<epoch>' returns a dictionary of the specific epoch data set requested with unique keys about its position and velocity data.
The route '/epochs/<epoch>/speed' returns the instantaneous speed for a specific epoch in the data set. 
The route '/delete-data' deletes all data from the data set. 
The route '/post-data' reloads the dictionary with data from the web.
The route '/comment' returns a 'comment' list object from ISS data.
The route '/header' returns a 'header' dict object from ISS data.
The route '/metadata' returns a 'metadata' dict object from ISS data.
The route '/epochs/<epoch>/location' returns latitude, longitude, altitude, and geoposition data for a given epoch.
The route '/now' returns latitude, longitude, altitude, and geoposition data for an epoch that is nearest in time.
```

In order to run the ```/delete-data``` route you must run the ```curl``` a little differently: ```curl -X DELETE localhost:5000/delete-data```. The output should be an empty dataset since it deletes the data:
```
[]
```
Check that the data set has actually been deleted by running ```curl localhost:5000/```.


The same unique curl command is the case for the ```/post-data``` route. Use the command ```curl -X POST localhost:5000/post-data```. Output:
```
the data has been posted
```
Check that the data set has actually been posted by running ```curl localhost:5000/```.



The ```/comment``` route outputs a list object of comments about the ISS data:
```
[
  "Units are in kg and m^2",
  "MASS=461235.00",
  "DRAG_AREA=1964.62",
  "DRAG_COEFF=4.00",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
…
]
```


The ```/header``` routes outputs the 'header' dictionary object from the ISS data:
```
{
  "CREATION_DATE": "2023-058T21:02:19.972Z",
  "ORIGINATOR": "JSC"
}
```


The ```/metadata``` route outputs the 'metadata' dictionary object from the ISS data:
```
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-058T12:00:00.000Z",
  "STOP_TIME": "2023-073T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```

The ```/epochs/50/location``` route outputs the latitude, longitude, altitude, and geolocation of a specific epoch. The geolocation will not be known if the ISS is over the ocean, so there are two possible outputs.
1:
```
{
  "altitude": {
    "units": "km",
    "value": -6364197.968864758
  },
  "geo": {
    "ISO3166-2-lvl4": "AU-QLD",
    "city_district": "Esmeralda",
    "country": "Australia",
    "country_code": "au",
    "municipality": "Croydon Shire",
    "state": "Queensland"
  },
  "latitude": -18.9743413534676,
  "longitude": 142.75833256176264
}
```
Or 2:
```
{
  "altitude": {
    "units": "km",
    "value": -6364196.111767501
  },
  "geo": "geo location is unknown, perhaps it is over the ocean",
  "latitude": -18.754409239452805,
  "longitude": -120.42065547090488
}
```

The ```/now``` route outputs the closests epoch to the current date and time and returns information about its location and speed:
```
{
  "closest_epoch": "2023-067T16:42:07.856Z",
  "location": {
    "altitude": {
      "units": "km",
      "value": -6364199.811651108
    },
    "geo": "geo location is unknown, perhaps it is over the ocean",
    "latitude": 0.4894663802027471,
    "longitude": -120.88028096429042
  },
  "seconds_from_now": 43.68109583854675,
  "speed": {
    "units": "km/s",
    "value": 7.6577609186199975
  }
}
```
