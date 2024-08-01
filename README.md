# WPI CS542 Summer 2024 Final Project

## SetUp

### Databse
1. Download and unzip the [tpch.db.zip](https://canvas.wpi.edu/courses/58982/files/6627919?module_item_id=1120250) file.
2. Move the unzipped tpch.db file to the data folder in this repo

Alternatively, we could use git lfs, but this seems more straightforward for now.

### Python Environment
1. Ensure [Anaconda](https://www.anaconda.com/) is installed
2. In the root of this repository, run the following
    ```bash
    conda env create -f environment.yaml
    conda activate cs542
    ```

### SQLite
If you use VSCode, install the SQLite extension by user alexcvzz.

Then, open the command palette (CTRL + SHIFT + P) and open the database, then use the database.

## Examples
See the examples folder on how to access the database.