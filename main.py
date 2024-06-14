#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py

"""
Description: Script used to query all clients data from a database and clean the
    invoice service 'factura.com' using the UID.
Author: Luis Maldonado.
Created on: Mon May  06 11:25:54 2024
Modified on: Tue May  09 11:16:01 2024
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
DATABASE_PORT = env_config.get('DATABASE_PORT')
DATABASE_USER = env_config.get('DATABASE_USER')
DATABASE_PASSWORD = env_config.get('DATABASE_PASSWORD')


################################## Constants ##################################
MAX_RETRIES = 3


################################## Instances ##################################
connection = Connection(host = DATABASE_HOST,
                        port = DATABASE_PORT,
                        user = DATABASE_USER,
                        password = DATABASE_PASSWORD,
                        database='pvunitelectronics')


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
    query_complement = 'WHERE sku = ""'

    result = connection.fetch_data(table = 'webhookproductos',
                                    fields = ['id', 'sku', 'last_modified_by'],
                                    filter_query = query_complement)
    print(result)
    result_copy = result.copy()
    result_copy['_fixed_price_rules'] = "Sin escalas"
    print(result_copy)

    insert_result = connection.insert_data(table='webhookproductos', data_df = result_copy)
    print(insert_result)
    
    delete_copy = result_copy.copy()
    delete_data = connection.delete_data(table='webhookproductos', data_df = delete_copy, field_to_operate = 'sku')
    print(delete_data)    
    
    exec_query = connection.execute_special_query(query='SELECT id, sku FROM webhookproductos WHERE last_modified_by LIKE "%Claudia%"')
    print(exec_query)
    
    exec_query = connection.execute_special_query(query='DELETE FROM webhookproductos WHERE sku = "OFERTA-315"')
    print(exec_query)
    
    truncate = connection.truncate_table(table='webhookproductos')
    print(truncate)
    

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
