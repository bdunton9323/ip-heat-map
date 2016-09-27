# ip-heat-map

IP Heatmap is an application that plots the locations of all the IP addresses in a given data set. This repository contains a large data set to work with.

## Architecture
The front end uses the javascript library [leaflet.js](http://leafletjs.com/) and [leaflet-heat.js](https://github.com/Leaflet/Leaflet.heat). The javascript gets the data by making an AJAX call to a REST endpoint hosted by a python application. The python application uses Tornado for the HTTP processing. The geolocation data is stored in a mongo database.

## Set up

This project requires python version 2.7 to run. It also requires virtualenv for running everything in a self-contained manner.

``` sh
> pip install virtualenv
```

### Set up the database
Extract the two CSV files from the included **GeoLiteCity-latest.zip** file to the 'geodata' directory.

Install [mongodb](https://www.mongodb.com/download-center#community) and run it. You must use a version greater than 2.4.
 - [Windows instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
 - [Linux instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-linux/)
 - [OSX instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
 
To populate the mongo database for the first time, or any time the data changes, run the Extract Transform and Load (ETL) script. There are separate scripts for the IPv4 data and the IPv6 data. The IPv4 data requires two files - one mapping IP address to location code, and the other mapping location code to geo coordinates. There is a batch file that calls both data import scripts. The batch file assumes mongo is running on `localhost:27017` and the data resides in `<projectroot>/geodata/ipv4` and `<projectroot>/geodata/ipv6`

```sh
> etl_full.bat
```

### Run the python web server

The server requires the following libraries, which will be installed in the virtual environment:
  - simplejson
  - tornado
  - pymongo

Install the server using the provided **runserver.bat** file (if you are on linux you'll have to write your own - I didn't have a linux system to test on). This will start the python virtual environment and run the server.


## Attributions
This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com.