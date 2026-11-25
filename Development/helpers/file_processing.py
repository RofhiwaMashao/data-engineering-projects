import os
import pandas as pd
import numpy as np
import sqlalchemy 
from datetime import datetime, timedelta, timezone
from helpers.logger import logger
from dotenv import load_dotenv
load_dotenv()
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import socket
from helpers.connectors import engine_from_postgres

execDir = os.path.abspath('')

def updateControl(control_type, DML_function, fileLoc=None, connection_object=None, record_id=None, records=None,
                  inserted_to=None, error_msg=None, **API_kwargs):
    '''After certain processes have been completed or failed, we want to update the control/reference tables with stats
    and record transaction details.
    
    :param control_type: Type of control table to update. Types are "API", "eMAIL", "Error", and "File
    :type control_type:
    
    
    
    '''