# NBA data insights

## Task description

1. Create a Python 3.* that parses the NBA statistics provided in the attached files
2. Dump the statistics into a MySQL database in a normalized format
3. Create a user facing functionality to retrieve the following data points:
	1. The best player in terms of productivity for each week of the selected season (each point/rebound/assist counts the same)
	2. Prediction of a match result between two teams (the prediction model is up to you to create, the more interesting, the best)
4. The program can be web facing (FLASK) or command line only


## How to replicate the enviroment?

- **Python Version:** Python 3.*

- **Enviroment:**

    Replicate the enviroment with `requirements.txt`
    ```
    # using pip
    $ pip install -r requirements.txt

    # using conda
    $ conda create --name <env_name> --file requirements.txt
    ```

## Project Skeleton

In a first approach, our ML models will be consumed through API Rest or through CLI. Based on this idea, the file structure is as follows

```raw  text
├─ README.md          <- The top-level README for this project.
├─ requirements.txt   <- Python library dependency
├─ src                <- Implemented python modules
├─ models             <- AI generated models
├─ data               <- Used data
└─ app                <- Entrypoint app
```

