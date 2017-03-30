#! /home/nisarg/Neil/env/bin/python


import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/nisarg/Neil_College/Flask/dbms/FlaskApp")

from FlaskApp import app
app.secret_key = "ksdufhohianl"


