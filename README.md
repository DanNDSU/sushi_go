# SushiGo RL #
Initial implementation of Sushi Go! by Martin Liu, as modified by Manveer Kaur and Dan Nygard.
Original code base can be found at: https://github.com/Gravellent/sushigo-rl

We recommend using Anaconda (https://www.anaconda.com/) to handle dependencies.

## Implementation and testing relies on installation of the following packages: ##
- Jupyter Notebook
- numpy
- scipy
- plotly
- torch
- psycopg2
    - You will also need to have postgres installed. DBUtils.py lists the connection details.
- pandas
- tqdm

A complete listing of all packages used in our Anaconda environment is in sushi_go_env.yml.

## How to run the game ##
- State.py handles the logic of the game
    - You can run one (or multiple) games by adjusting the main method in State.py as you'd like, and running $python State.py  
- Player package include a variety of agents that interacts with env. to play the game
    - If you add another player class, make sure to include it in __init__.py
- utils.py contains many useful functions for the game, including the distribution of cards and score calculation
- DBUtils.py contains database connection information
- test.ipynb is (slightly modified) the Jupyter Notebook of Liu's original training and evaluation games
- extended_test.ipynb contains further tests of our learning rate and reward function variations
    - There are a number of other notebook (.ipynb) files containing our experiments:
    - DB_againstAllPlayers.ipynb is a jupyter notebook where we play our Q Player with DB against all other players.
    - DB_withOtherQPlayers.ipynb is where we play our different Q Players against each other.
