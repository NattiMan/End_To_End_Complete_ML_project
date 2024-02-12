import logging
import os
import datetime


ct = datetime.datetime.now()
LOG_FILE=f"log_{ct.strftime('%Y%m%d_%H%M%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    encoding='utf-8',
    level=logging.INFO,

)
