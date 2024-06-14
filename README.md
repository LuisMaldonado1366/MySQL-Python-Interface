# MySQL-Python-Interface


## Description
Custom python module integration to interact with mysql.connector for databases management.


## Author
- **Author:** Luis Maldonado
- **Created on:** Thu Aug 31 14:24:05 2023
- **Modified on:** Thu June  13 12:53:36 2024
- **Version:** 2.0.0


## Features
- Retireves data from a given table as a pandas dataframe.
- Deletes data from a table based on a pandas dataframe column.
- Truncate the specified table.
- Inserts pandas dataframe into a table.
- Handles errors and retries accordingly to different situations.


## Dependencies
- Python 3.11.4
- pandas 2.0.2
- mysql-connector 2.2.9
- python-decouple 3.8


## Modules and Instances
- Standard: `json`, `sys`, `os.path`, `time.sleep`, `datetime`.
- Third-party: `pandas`, `decouple.Config`, `decouple.RepositoryEnv`.


## Instances
- Environment Configuration: `env_config` (`decouple.Config`).
- Database Connection: `connection` (`connection`).


# Constants
- DATABASE_HOST: Database host.
- DATABASE_PORT: Database port.
- DATABASE_USER: env_config.get('DATABASE_USER')
- DATABASE_PASSWORD: env_config.get('DATABASE_PASSWORD')
- DATABASE_NAME: env_config.get('DATABASE_PASSWORD')


# Functions
1. fetch_data(table: str, **kwargs: list) -> pd.DataFrame.
- Retrieve data from a specified database table.
2. insert_data(table: str, data_df: pd.DataFrame) -> bool.
- Inserts the given pandas dataframe into the given table.
3. delete_data(table: str, data_df: pd.DataFrame, field_to_operate: str) -> bool.
- Deletes the given data from the specified table database using as key the passed field.
4. truncate_table(table: str) -> bool.
- Truncates the given table.
5. execute_custom_query(self, query: str) -> any.
- Excutes a custom SQL query.


# Main Execution
The example script (main.py) manipulates a table database using all the commands.


## Configuration
For the configuration there must be some steps.
1. Clone the repository to your local machine.

2. Set up the environment variables by creating a .env file with the necessary database cradentials, use the given .env.example.

3. Set up the necessary tables and database if not already created.


## Usage
1. Set up the database connection and provide the necessary credentials.



## License
Not licensed yet.