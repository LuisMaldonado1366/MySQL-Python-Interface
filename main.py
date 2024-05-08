#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py

"""
Description: Script used to query all clients data from a database and clean the
    invoice service 'factura.com' using the UID.
Author: Luis Maldonado.
Created on: Mon May  06 11:25:54 2024
Modified on: Tue May  07 17:19:25 2024
Version: 1.0.0
Dependencies: json, sys, time, datetime, decouple, connection.
"""


################################## Libraries ##################################
# Standard.
import sys
from os.path import split
from time import sleep
from datetime import datetime

# Third-party.
from decouple import Config, RepositoryEnv

# Custom.
from connection import Connection


################################## Enviroment variables ##################################
env_config = Config(repository = RepositoryEnv(source = '.env'))
DATABASE_HOST = env_config.get('DATABASE_HOST')
DATABASE_USER = env_config.get('DATABASE_USER')
DATABASE_PASSWORD = env_config.get('DATABASE_PASSWORD')
DATABASE_NAME = env_config.get('DATABASE_NAME')
BROKER_HOST = env_config.get('BROKER_HOST')
BROKER_PORT = env_config.get('BROKER_PORT')
TOPIC_SUBSCRIBE = env_config.get('TOPIC_SUBSCRIBE')
TOPIC_PUBLISH = env_config.get('TOPIC_PUBLISH')


################################## Constants ##################################
MAX_RETRIES = 3


################################## Instances ##################################
connection = Connection(host = DATABASE_HOST,
                        user = DATABASE_USER,
                        password = DATABASE_PASSWORD)


################################## Functions ##################################
def log_out(*, message: str, identifier: str) -> None:
    """
    Resume: Print a message along with the current timestamp.
    Description: This function receives a message to be shown in console along
        with the timestamp.
    Args:
        message (str): Text to be displyed.
        identifier (str): Symbol to be put between brackets to make it easier to
            identify an specyfic message.

    Returns:
        None
    """
    dt_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print (f'\n{dt_log} - [{identifier}] {message}')

    
def retrieve_data(*, db_host: str = 'local_host', db_user: str = 'root',
                  db_password: str = '', database: str, table: str, **kwargs) -> object:
    """
    Resume: Retrieve data from the specified database and table.
    Description: This function uses the db credentials and 
                    retrieves the fields of the indicated table.
    Args:
        database (str): Name of the database.
        table (str): Name of the table to query.
        **kwargs: Additional keyword arguments:
            - query_fields (list): List of fields to retrieve.
            - database_credentials (dict): Database connection credentials.

    Returns:
        pandas.DataFrame: DataFrame containing the retrieved data.
    """
    connection_retrieve = Connection(host = db_host,
                                     user = db_user,
                                     password = db_password)

    if 'query_fields' in kwargs:
        results_fields = kwargs['query_fields']
        results_db = connection_retrieve.fetch_data(database = database,
                                                    table = table,
                                                    fields = results_fields)
    else:
        results_db = connection_retrieve.fetch_data(database = database,
                                                    table = table)
    return  results_db


def main():
    """
    Resume: Main execution loop for processing the cleaning data process.
    Description: This function sets up the database consuming process and starts
        trhe cleaning of the clients registered in 'factura.com'.
    Args: 
        None

    Returns:
        None
    """
    user = 'Aracely'
    sku = 'AR0001'
    query_complement = f'''WHERE last_modified_by LIKE "%{user}%" and sku = "{sku}"'''

    result = connection.fetch_data(database = 'pvunitelectronics',
                                   table = 'webhookproductos',
                                   fields = ['id', 'sku', 'last_modified_by'],
                                   filter_query = query_complement)
    print(result)
    result_copy = result.copy()
    result_copy['_fixed_price_rules'] = "Sin escalas"
    print(result_copy)

    insert_result = connection.insert_data(database = 'pvunitelectronics', table='webhookproductos', data_df = result_copy)
    print(insert_result)
    

##################################### Main ####################################

# Main program.
if __name__ == '__main__':
    RETRIES = 0
    while RETRIES < MAX_RETRIES:

        try:
            main()
            sys.exit(0)

        except KeyboardInterrupt:
            log_out(message = 'Keyboard interruption', identifier = 'x')
            sys.exit(0)

        except Exception as error:
            result_message = f'{error.__class__.__name__}'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = split(exc_tb.tb_frame.f_code.co_filename)[1]
            RETRIES += 1
            log_out(message = \
                    f'''Exit on error: {result_message} - {error.args})
                        Filename: {fname} - {exc_tb.tb_lineno}''',
                        identifier = 'x')

        finally:
            log_out(message = 'Finished execution.', identifier = 'x')
            sleep(5)

# End-of-file (EOF)