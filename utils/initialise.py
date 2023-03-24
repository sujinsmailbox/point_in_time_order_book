import csv
import glob
import logging
import os
from datetime import datetime
from config.config import *
from sql_writer import MySQLWritter

logging.basicConfig(level='INFO', format='%(asctime)s | %(levelname)s | %(message)s')

def _run_ddl_statements():
    directory_path = system_config['ddl_path'] #We can have a vallidator function in the config for getting all the variables
    pattern = "*.sql"

    sql_writter = MySQLWritter(system_config['connection_config']['host'], system_config['connection_config']['user'], system_config['connection_config']['password'], system_config['connection_config']['database'], system_config['connection_config']['port'])
    files = glob.glob(os.path.join(directory_path, pattern))

    if len(files) == 0:
        logging.warning("no sql files for executing")
        return
    for file in files:
        with open(file, 'r') as file:
            logging.info(f"executing {file}")
            sql_string = file.read()
            logging.info("Executing")
            logging.info(sql_string)
            sql_writter.execute_sql(sql_string)
    logging.info("completed executing all the DB patch files")

def _insert_batch_data():
    directory_path = system_config['data_path']  # We can have a vallidator function in the config for getting all the variables
    pattern = '*.csv'
    files = glob.glob(os.path.join(directory_path, pattern))
    for file in files:
        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            rows = []
            sql = """INSERT INTO order.quotes (symbol
                                    ,marketCenter
                                    ,bidQuantity
                                    ,askQuantity
                                    ,bidPrice
                                    ,askPrice
                                    ,startTime
                                    ,endTime
                                    ,quoteConditions
                                    ,sipFeed
                                    ,sipFeedSeq ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            sql_writter = MySQLWritter(system_config['connection_config']['host'], system_config['connection_config']['user'], system_config['connection_config']['password'],
                                       system_config['connection_config']['database'], system_config['connection_config']['port'])

            for i, row in enumerate(reader):
                row[6] = datetime.fromisoformat(row[6][:-1]).strftime('%Y-%m-%d %H:%M:%S')
                row[7] = datetime.fromisoformat(row[7][:-1]).strftime('%Y-%m-%d %H:%M:%S')
                rows.append(row)
                if (i+1) % 10000 == 0:
                    sql_writter.execute_batch_sql(sql, rows)
                    rows.clear()
            if rows:
                logging.info(f"printing remaining {len(rows)} rows")
                sql_writter.execute_batch_sql(sql, rows)


def load_initial_data():
    _insert_batch_data()
    #placeholder function for calling other sub systems if required

def patch_database():
    #if patching already not done  ( placeholder to check inn database to see if patching is done and what version is it
    _run_ddl_statements()


if __name__ == "__main__":
    pass

