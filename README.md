# MySQL-Python-Interface

## Description

Custom python module to interact with mysql databases.

## Author

- **Author:** Luis Maldonado
- **Created on:** Thu Aug 31 14:24:05 2023
- **Modified on:** Tue May  09 11:16:01 2024
- **Version:** 1.2.3

## Features

- 
- 
- 
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

- Maximum Retries: MAX_RETRIES
- Retries: RETRIES
- Database Credentials: DATABASE_CREDENTIALS



# Functions

1. retrieve_data(database, table, **kwargs).
- Retrieve data from a specified database table.
2. execute_phase(stage).
- Creates an RPC object and starts procedure (RPC) to the master server.
3. StockUpdateRpcClient::__init__().
- Constructor for the RPC class to handle AMQP messages.
4. StockUpdateRpcClient::on_response(response_channel, method, props, body).
- Callback function for processing messages received from the AMQP broker on response.
5. StockUpdateRpcClient::call(self, operation):
- Starts the RPC to the master's queue and waits for the response of the message sent.
6. main().
- Main execution loop for processing messages received from AMQP.

# Main Execution

The script sents a message to the specified queue and waits for the response. It handles retries in case of connection errors and saves the log to the docker logs file.

## Configuration

For the configuration there must be some steps.
1. Clone the repository to your local machine.

2. Set up the environment variables by creating a .env file with the necessary database cradentials and store it in the "app" folder, Database credentials should be provided in the .env file, which means a json containing `host`, `user` and `password`.

3. Set up the necessary tables in the database ("*stock_update_result*", "*stock_update_config*") if not already created.

6. Build the docker image and get the container up and running using the `sh` command:

```bash 
sh stock_update_crontab.sh
```


## Usage

1. Ensure that the RabbitMQ server is running and accessible and that you have the right credentials stored y the config table at the database.
2. Set up the database connection and provide the necessary credentials.
3. Monitor the container is up and running.


## License

Not licensed yet.