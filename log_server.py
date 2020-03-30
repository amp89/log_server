from flask import Flask
import loggers
import sys
from flask import request
app = Flask(__name__)
import importlib
import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter("")
import datetime
import time
import os

import threading
from utils import *

def do_log(log_name, post_data):
    log_obj = get_log_obj(log_name=log_name)
    levelname = post_data["levelname"]
    log_str = get_log_str(post_data=post_data)
    log_func = getattr(log_obj,levelname.lower())
    log_func(log_str)
    
@app.route('/log', methods=["POST"])
def hello_world():
    log_name = request.args.get("name")
    # key = request.args.get("key")
    key = request.headers.get("Authorization").split(" ")[-1]

    logger_data = importlib.import_module(f"loggers.{log_name}").logger_data
    assert isinstance(logger_data,dict)
    assert key == logger_data["key"] 

    post_data = request.form   

    # t = threading.Thread(target=do_log, args=(log_name, post_data, log_data,))
    # t.daemon = True
    # t.start()
    do_log(log_name, post_data)

    do_callbacks(log_name=log_name, callback_list=logger_data["callbacks"], post_data=post_data)

    return app.response_class(
        response=None,
        status=200,
        mimetype='application/json'
    )
    

if __name__ == '__main__':
    
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=True)