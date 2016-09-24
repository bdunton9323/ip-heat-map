# ip-heat-map

Install the server using the provided **installserver.bat** file. This will start the virtual environment and run the server.

Extract the two CSV files from GeoLiteCity-latest.zip to the 'geodata' directory.

Start a mongo server.

Run the Extract Transform and Load (ETL) script, etl.py to load the data into mongo.

I did not have a linux system to test on, so I only provided a Windows batch file for installing the web server.

The server requires the following libraries, which will be installed in the virtual environment:
  - simplejson
  - tornado
  - pymongo
