virtualenv etlenv
call etlenv\Scripts\activate.bat
pip install pymongo
python etl4.py ..\geodata\ipv4\GeoLiteCity-Blocks.csv ..\geodata\ipv4\GeoLiteCity-Location.csv mongodb://localhost:27017
python etl6.py ..\geodata\ipv6\GeoLiteCityv6.csv mongodb://localhost:27017
call etlenv\Scripts\deactivate.bat