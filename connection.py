# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# connection.py

"""
Description: 
Author: Luis Maldonado
Created on: Thu Aug 31 14:24:05 2023
Modified on: Thu May 02 16:06:51 2024
Version: 1.1.2
Dependencies: pandas, mysql.connector.
"""

################################## Libraries ##################################
# Third party.
import pandas as pd
from mysql.connector import Error, connect


################################### Classes ###################################
class Connection:
    """
    A class for connection and managment of a mysql database.

    Attributes:
        _host (str): 
        _user (str):
        _password (str): 
    """

    def __init__(self, host, user, password):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
           
        Returns:
            None
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.__connection = None
        self.__database = None
        self.__cursor = None
        self.__fields = []


    def __connect(self, database):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        try:
            self.__database = database
            self.__connection = connect(
                host = self.__host,
                #port = 3306,
                user = self.__user,
                password = self.__password,
                db = self.__database
            )

        except Error as ex:
            print(f"Error al intentar la conexion {format(ex)}")

        return self.__connection


    def __create_cursor(self, database):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        self.__database = database
        _connection = self.__connect(self.__database)
        self.__cursor = _connection.cursor()

        return self.__cursor


    def fetch_data(self, database, table, **kwargs):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        self.__database = database
        _table = table
        self.__cursor = self.__create_cursor(self.__database)

        _str_query = 'SELECT '

        if 'fields' in kwargs:
            self.__fields = kwargs['fields']
            for field in self.__fields:
                _str_query += field + ', '
            _str_query = _str_query[:-2]
        else:
            _str_query += '*'

        _str_query += ' FROM ' + _table

        self.__cursor.execute(_str_query)

        _results = self.__cursor.fetchall()

        _result_df = pd.DataFrame(data = _results, columns = self.__cursor.column_names)

        self.__connection.close()
        self.__cursor.close()

        return _result_df


    def insert_data(self, database, table, data_df):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        try:
            self.__database = database
            self.__cursor = self.__create_cursor(self.__database)
            self.__fields = str(list(data_df.columns)).\
                translate(str.maketrans({'[': '(', ']': ')'}))
            self.__fields = self.__fields.replace("'", "")
            _str_query_complement = ''
            for field in range(len(data_df.columns)):
                _str_query_complement += '%s, '
            _str_query_complement = _str_query_complement[:-2]

            _values = []

            for index in range(data_df.shape[0]):
                var = []
                for col in data_df.columns:
                    if data_df.iloc[index][col] is None:
                        temp_var = None
                    elif isinstance(data_df.iloc[index][col], int):
                        temp_var = int(data_df.iloc[index][col])
                    else:
                        temp_var = str(data_df.iloc[index][col])
                    var.append(temp_var)
                _values.append(tuple(var))

            _str_query_values = ''
            for field in data_df.columns:
                _str_query_values += f'{field} = VALUES({field}), '
            _str_query_values = _str_query_values[:-2]

            _str_query = (f"INSERT INTO {table} "
                f"{self.__fields} "
                f"VALUES ({_str_query_complement}) "
                f"ON DUPLICATE KEY UPDATE {_str_query_values};")

            self.__cursor.executemany(_str_query, _values)
            self.__connection.commit()

            _result = True

        except Error as error:
            print(f'Database update failed: {format(error)}')
            self.__connection.rollback()
            _result = False

        self.__connection.close()
        self.__cursor.close()

        return _result


    def delete_data(self, database, table, data_df, field_to_operate):
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        _database = database
        _table = table
        self.__cursor = self.__create_cursor(_database)
        _data_df = data_df.copy()
        _field_to_operate = field_to_operate
        _values = str(list(_data_df[_field_to_operate])).\
            translate(str.maketrans({'[': '(', ']': ')'}))
        _str_query =\
            f'DELETE FROM {_table} WHERE {_field_to_operate} IN {_values}'

        self.__cursor.execute(_str_query)
        self.__connection.commit()

        self.__connection.close()
        self.__cursor.close()

        return self.__cursor.rowcount == _data_df.shape[0]

# End-of-file (EOF)
