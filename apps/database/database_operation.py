import sqlite3
import csv
from os import listdir
import shutil
import os

from apps.core.logger import Logger

class DatabaseOperation:
    """_summary_
    **************************************************************************
    *
    *filename:       database_operation.py
    *version:        1.0
    *author:         Daniel Rawlins
    *creation date:  12-Jan-2024
    *
    *change history:
    *
    *who           when           version    change(include bug# if apply)
    *----------    -----------    -------    -----------------------------
    *D. Rawlins    12-JAN-2024       1.0     initial creation
    *
    *
    *description: Class to handle database operations
    *
    **************************************************************************
    """
    
    def __init__(self, run_id, data_path, mode):
        self.run_id = run_id
        self.data_path = data_path
        self.logger = Logger(self.run_id, 'DatabaseOperation', mode)
    
    def database_connection(self, database_name):
        """
        *method: database_connection
        *description: method to build database connection
        *return: Connection to the DB
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    12-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   database_name:
        """
        try:
            conn = sqlite3.connect('apps/database/'+database_name+'.db')
            self.logger.info("Opened %s database successfully" %database_name)
        except ConnectionError:
            self.logger.info("Error while connecting to database: %s" %ConnectionError)
            raise ConnectionError
        return conn
    def create_table(self, database_name, table_name, column_names):
        """
        *method: create_table_db
        *description: method to create database table
        *return: none
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    12-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   database_name:
        *   column_names:
        """
        try:
            self.logger.info('Start of Creating Table...')