# TD 3 - Exploring NoSQL

This page sets up your machine for the graded NoSQL lab, a series of Jupyter notebooks on Redis, MongoDB and OrientDB in the [lyon2-nosql](https://github.com/andfanilo/lyon2-nosql) repository.

![](./images/nosql-cover.jpg)

## Objectives

- [ ] Install the NoSQL tutorial environment with uv
- [ ] Start Redis, MongoDB and OrientDB with docker compose
- [ ] Connect to each database from a notebook
- [ ] Start the graded lab

## Prerequisites

- Git, uv and Docker, from [TD 0](prerequisites.md)

---

## 1. Install the tutorial

!!! note "Exercise - Install the Python environment"
    1. From your workspace folder, clone the tutorial, then browse into it:

        ```bash
        git clone https://github.com/andfanilo/lyon2-nosql
        cd lyon2-nosql
        ```

    2. Run `uv sync`. Open `pyproject.toml`: which package is the Python client of each database?

---

## 2. Start the databases

Each database runs in its own container. The `docker-compose.yml` file of the tutorial starts all three.

!!! note "Exercise - Start the databases with docker compose"
    1. Open `docker-compose.yml`. Which image and which ports does each service use?
    2. Start the databases in the background with `docker compose up -d`.
    3. Run `docker compose ps`. You should see the `redis`, `mongo` and `orientdb` services, each with the status `Up`.
    4. The `mongo` service mounts the `data` folder into its container. Before you run it, predict what `docker compose exec mongo ls /data/import` prints. Run it to check.

!!! question
    - Why don't you need to install Redis, MongoDB or OrientDB on your machine?
    - What happens to the data in your databases when you run `docker compose down`?

---

## 3. Check your setup

!!! note "Exercise - Connect to each database"
    1. From the `lyon2-nosql` folder, run `uv run jupyter lab`. To use VS Code instead, select the `.venv` environment as in the [Spark setup](spark.md#b-option-b-vs-code).
    2. Create a new notebook and run:

        ```python
        import pymongo
        import pyorient
        import redis

        r = redis.Redis(host="localhost", port=6379)
        print(r.ping())

        client = pymongo.MongoClient("localhost", 27017)
        print(client.server_info()["version"])

        orient = pyorient.OrientDB("localhost", 2424)
        orient.connect("root", "root")
        print(orient.db_list())
        ```

        - The first line must be `True`, and the second line a MongoDB version that starts with `8`. The third line lists the OrientDB databases.
        - The first time you import `pyorient`, it prints `SyntaxWarning` lines. The library is old. You can ignore them.

    3. Delete your notebook.

!!! warning "Common errors"
    - `ConnectionRefusedError`, `ServerSelectionTimeoutError` or `PyOrientConnectionException`: the database container doesn't run. Check with `docker compose ps`, then start it with `docker compose up -d`.
    - `port is already allocated` when you run `docker compose up -d`: another container uses the port, for example a MongoDB container from [TD 1](mlops.md). Find it with `docker ps`, then stop it with `docker rm -f <container id>`.

---

## 4. Start the graded lab

The graded lab is the series of notebooks in the `notebooks` folder. Do them in order: `1-redis.ipynb`, `2-mongo.ipynb`, then `3-orientdb.ipynb`.

When you finish a session, stop the databases with `docker compose down`.

---

## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Install the NoSQL tutorial environment with uv
    - [x] Start Redis, MongoDB and OrientDB with docker compose
    - [x] Connect to each database from a notebook
    - [x] Start the graded lab
