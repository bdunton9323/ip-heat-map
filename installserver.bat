virtualenv serverenv
call serverenv\Scripts\activate.bat
pip install simplejson
pip install tornado
pip install pymongo
python server.py
call serverenv\Scripts\deactivate.bat