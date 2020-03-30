from flask import Flask
import loggers
import sys
from flask import request
import importlib
import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter("")
import datetime
import time
import os

import threading
from multiprocessing.pool import ThreadPool

def get_log_str(post_data):
    name = post_data["name"]
    msg = post_data["msg"]
    args = post_data["args"]
    levelname = post_data["levelname"]
    levelno = post_data["levelno"]
    pathname = post_data["pathname"]
    filename = post_data["filename"]
    module = post_data["module"]
    exc_info = post_data["exc_info"]
    exc_text = post_data["exc_text"]
    stack_info = post_data["stack_info"]
    lineno = post_data["lineno"]
    funcName = post_data["funcName"]
    try:
        created = float(post_data["created"])
    except:
        created = time.time()
    msecs = post_data["msecs"]
    relativeCreated = post_data["relativeCreated"]
    thread = post_data["thread"]
    threadName = post_data["threadName"]
    processName = post_data["processName"]
    process = post_data["process"]

    log_now = str(datetime.datetime.fromtimestamp(created))

    log_str = f"{log_now} UTC|{levelname}|{name}|{filename}|{module}|{funcName}|{lineno}|{thread}|{threadName}|{processName}|{process}|{msg}"

    return log_str
    
def get_log_obj(log_name):
    log_obj = logging.getLogger(log_name)
    log_obj.setLevel(logging.DEBUG)
    log_dir_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"logs"),log_name)
    log_path = os.path.join(log_dir_path, f"{log_name}.log")
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)

    handler = RotatingFileHandler(log_path, maxBytes=50000000, backupCount=10)
    handler.setFormatter(formatter)
    log_obj.addHandler(handler)
    return log_obj


def do_callbacks(log_name, callback_list, post_data):
    # tp = ThreadPool(1)
    for callback_function in callback_list:
        # callback_function(log_name, post_data)
        # tp.apply_async(callback_function, (log_name, post_data,))
        t = threading.Thread(target=callback_function, args=(log_name, post_data,))
        t.daemon = True
        t.start()
    # tp.close()
        