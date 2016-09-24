virtualenv etlenv
call etlenv\Scripts\activate.bat
pip install pymongo
python etl.py
call etlenv\Scripts\deactivate.bat