# NBA data insights

## Task description

1. Create a Python 3.* that parses the NBA statistics provided in the attached files
2. Dump the statistics into a MySQL database in a normalized format
3. Create a user facing functionality to retrieve the following data points:
	1. The best player in terms of productivity for each week of the selected season (each point/rebound/assist counts the same)
	2. Prediction of a match result between two teams (the prediction model is up to you to create, the more interesting, the best)
4. The program can be web facing (FLASK) or command line only

## Project Skeleton

In a first approach, our ML models will be consumed through API Rest or through CLI. Based on this idea, the file structure is as follows

```raw  text
├─ requirements.txt   <- Python library dependency
├─ README.md          <- The top-level README for this project.
├─ makefile           <- Shortcuts
├─ src                <- Implemented python modules
├─ models             <- AI generated models
├─ eda                <- Generated notebooks for exploratory data analysis
└─ data               <- Used data
```

## How to replicate the enviroment?

- **Python Version:** Python 3.8.*
- **Enviroment:**

1. Replicate python enviroment with `requirements.txt`
    ```
    # using pip
    $ pip install -r requirements.txt

    # using conda
    $ conda create --name <env_name> --file requirements.txt
    ```
2. Export enviroment variables
	```
    export MYSQL_USER=?
	export MYSQL_PASSWORD=?
	export MYSQL_ROOT_PASSWORD=?
	export MYSQL_DATABASE=?
	export MYSQL_PORT=?
	export MYSQL_HOST=?
    ```
    NOTE: These variables are defined in `database.conf` file

## Database

1. Copy the  `database.conf` file to `src/mysql_db` folder
2. Create a mysql container

    ```
    $ docker-compose --file src/mysql_db/docker-compose.yml up  --build -d
    ```

3. Dump data to Database

    ```
    $ cd src/server
    $ python populate_database.py
    ```
## Server

1. Run flask server application
    ```
    $ export FLASK_APP=src/server/server.py
    $ flask run
    ```
2. Postam collection with examples https://www.getpostman.com/collections/5d81d74ebf90f6a7649b
