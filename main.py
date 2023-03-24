import csv
import glob
import logging
import os
import time
from datetime import datetime
from config.config import *
from utils.initialise import patch_database, load_initial_data
from process_data import ProcessData


logging.basicConfig(level='INFO', format='%(asctime)s | %(levelname)s | %(message)s')


def get_input():
    date_string = input(f'Give the input date in the format YYYY-MM-DD HH:MM:SS: \n')
    symbol_name = input(f'Please input a symbol name. eg AAPl: \n')
    try:
        time_stamp = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        time_stamp =  time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        return symbol_name, time_stamp
    except ValueError:
        logging.error("unable to cast the string to timestamp")
        get_input()


if __name__ == "__main__":
    logging.info("patching the database")
    # patch_database()
    logging.info("loading the initial data")
    # load_initial_data()
    logging.info("data load complete")
    logging.info("*" * 100)

    while True:
        logging.info("Please provide a date and a symbol name") #eg AAPL, '2021-02-18 10:00:35'
        symbol_name, time_stamp = get_input()
        order_data = ProcessData(time_stamp, symbol_name)
        order_data.process()
        logging.info("*" * 100)




