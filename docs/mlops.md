# TD 4 - MLOps

## Prerequisites

Make sure you have the following commands working on your workstation:

- conda
- docker 
- docker-compose

## 1. Docker

### a. Your first Docker commands

![](./images/docker-logo.png)

Before starting, make sure your command line has `docker` and `docker-compose` working.

!!! note "Exercise - Your first Docker commands"
    - List the available docker commands by running `docker`.
    - Run the `docker images` command. This should list all your existing Docker images you can use. Do you have any? Compare them with the images in your `Docker Desktop` window.
    - Run the `docker ps -a` command. Do you see any previously running containers?
        - The `ps` command stands for `process`, you can imagine this like a running container. The `-a` flag stands for *all containers*, not only running ones. You should see containers that were stopped earlier.

We want to test the new walrus operator in Python 3.8. You can download any Docker image from [the Docker Hub](https://hub.docker.com/).

Go check the [Python image](https://hub.docker.com/_/python) for example.

![](./images/docker-tags.PNG)

To run a Docker image, you'll need to specify its name and tag as `<label>:<tag>`. Let's run some code in the `python:3.8-slim` image, as you can guess a _small_ image with Python 3.8 installed.

!!! note "Exercise - Run your first container"
    - Find the [command](https://docs.docker.com/engine/reference/commandline/pull/) to download the `python:3.8-slim` image in your set of available images.
        - Check the image is available with `docker images`
    - Run a container from the image with `docker run -it --rm python:3.8-slim`.
    - By default the `run` will put you in a Python shell. Try to run some Python code and play with the walrus operator.
        - Docker gives you an easy way to test new Python versions without installing it on your system.
    - Exit the container by typing `exit()` in the command. Make sure the container has disappeared with `docker ps -a`.
    - Using the [Docker run help](https://docs.docker.com/engine/reference/run/), find out the role of the `--rm` and `-it` (an abbreviation for `-i -t`) flag in the run command.
    - Run `docker run -it --name test python:3.8-slim` and then exit the container. What displays this time in `docker ps -a` ?
    - Since we gave a name to our container, let's restart it with `docker start test`. You can then reattach to it with `docker attach test`.
    - We had enough fun with that container, destroy it by using the `docker rm` command.
    - Let's clean up our images a little bit, delete the `python:3.8-slim` image with the `docker rmi` command.

Most of the open-source technologies have a dedicated Docker image maintained by the community. Do not hesitate to browse the Docker Hub to test the latest systems.

What if you want to use a Python image but don't want to use its Python shell?

!!! note "Exercise - Changing the CMD of the image"
    - In an Anaconda prompt, run `python -m http.server 9999`. In a browser, connect to `localhost:9999`. What is the point of this command? Close the server afterwards.
    - Let's run this command in a Docker container! Run `docker run -it --rm -p 9999:9999 python:3.8-slim python -m http.server 9999`. connect to `localhost:9999` in your browser.
    - What is the `-p 9999:9999` flag? What happens if you put `-p 7777:9999`?

This way we now can download an image, run it with a custom command and expose some of the ports to us.

!!! danger "Challenge"
    - In a folder with some Python notebooks you copied from some other projects you want to use, run the following command: `docker run -v $PWD:/tmp/working -w=/tmp/working --rm -it -p 8888:8888 kaggle/python jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="" --notebook-dir=/tmp/working`.
        - This is the notebook that is used by Kaggle notebooks, with all the necessary Data Science packages to work on your projects!
        - Carefully read each part of the command and prepare to be able to explain each part to me.
        - The only flag you currently don't know is `-v`. It mounts one of your local folders to a folder inside the running container, so that you can see your local Jupyter notebooks from inside the containers. You can edit a file in the Jupyter notebook and see the changes locally (though I don't recommend doing it like this because of line separator risks).

### b. Your first Dockerfile

Our goal is to create our own Docker image, using a `Dockerfile`.

!!! note "Exercise - Folder architecture"
    - Put yourself in a brand new folder, like `mlops-td`. 
    - In this `mlops-td` folder, create a new folder, name it however you like. For example `td`. The `mkdir <name>` will do the trick
    - Create the following empty files:

    ```
    td
     ├── app.py             <- A python script
     └── Dockerfile         <- Has the Docker commands to build our custom image
    ```

    - Write some Python code in `app.py`. Something like `print('Hello world')`.

!!! note "Exercise - Dockerfile"
    - Open the `Dockerfile` file with your favorite editor.
    - Write down the following lines:
        - `FROM` specifies the parent image
        - `COPY` copies files or directories from the folder you ran docker from, into the image
        - `WORKDIR` puts the image location to the desired folder. Here, all future commands will be run inside the `/app` folder, like if you did a `cd /app`.
        - `RUN` runs a classic command
        - `CMD` defines the command the Docker container will run.
        - There are some more [here](https://docs.docker.com/engine/reference/builder/)

    ```Dockerfile
    FROM python:3.8-slim

    COPY app.py /app/app.py

    WORKDIR /app 

    RUN pip install rich

    CMD ["python", "app.py"]
    ```

    - To run the building of the image, run `docker build -t td ./`
        - the `-t` is the label and tag of the image.
        - the `./` specifies the folder which contains the `Dockerfile` to build. You should already be in the said folder.
    - Make sure the new `td` image was created. What is the size of the image? The command is similar to one used in a previous section.
    - Run your new image! The command is similar to one used in a previous section.
    - Docker build work in layers. Edit or duplicate the `RUN pip install rich` line to add some more dependencies (like, install `pandas` or `numpy` or something cool). When you rerun the same `build` command, do you notice something in the print output? You should see ` ---> Using cache` appear in particular places, telling you it didn't start the build from scratch.
        - Useful when you have Dockerfiles with around 100 commands [like the Kaggle/python one](https://github.com/Kaggle/docker-python/blob/main/Dockerfile.tmpl)

!!! danger "Challenge"
    - Create a Docker image which copies your `Pyspark` Jupyter notebooks and the `pyspark` + `jupyter` dependencies. When opened, a Jupyter lab server should run, all your Pyspark projects at the root that I can immediately `Run All`. _In theory, all you need to do afterwards is send me the built image_
        - NB: I tried using [this image](https://hub.docker.com/r/jupyter/pyspark-notebook) but couldn't get to work it out. I managed to install Java 8 in a Python image but it's a bit complicated...so feel free to jump the question if you spend more than 1h building the answer

### c. Your first docker-compose

With `docker-compose`, you are able to run a group of containers altogether. In this tutorial, we will setup a 3-tier architecture with Docker compose.

![](./images/three-tier-architecture.png)

!!! note "Exercise - Architecture"
    - Build the following folder architecture
    ```
    client
    ├── app.py             <- Streamlit/Gradio/Panel/Dash/Shiny to request a REST API
    └── Dockerfile         <- Commands to build our custom image
    
    server
    ├── app.py             <- FastAPI to expose a REST API that will write to MongoDB
    └── Dockerfile         <- Commands to build our custom image

    docker-compose.yml
    ```

!!! note "Exercise - Build a Python REST API"
    - In `server/app.py`, create a REST API with [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) so that, when you run `uvicorn --host 0.0.0.0 app:app` locally, you can connect to `http://localhost:8000` and get back `Hello World`.

    ??? abstract "Solution ONLY if you feel stuck"
        Content of `server/app.py`:
        ```python
        from fastapi import FastAPI

        app = FastAPI()


        @app.get("/")
        async def root():
            return {"message": "Hello World"}
        ```

    - In `server/Dockerfile`, install FastAPI+uvicorn and run the command that runs the server.
    - Build your image. Give it a name like `mlops:server`. Make sure if you run the container with the correct port exposed, you can connect to the API from the browser and get your `Hello world`.

    ??? abstract "Solution ONLY if you feel stuck"
        Build with `docker build -t mlops:server .` . Run with `docker run -p 8000:8000 --rm mlops:server`. 
        ```Dockerfile
        FROM python:3.8-slim

        COPY app.py /app/app.py

        WORKDIR /app 

        RUN pip install uvicorn fastapi

        CMD ["uvicorn", "--host", "0.0.0.0", "app:app"]
        ```

!!! note "Exercise - Using Docker compose to run a server + Mongodb"
    - Add the following code in `docker-compose.yml`. This will start a Mongodb next to your server image:
    
    ```yaml
    version: '3.1'

    services:

        mongo:
            image: mongo
            restart: always

        server:
            image: mlops:server
            restart: always
            ports:
            - 8000:8000
    ```

    - Run the cluster with `docker-compose up`, from the root folder (where `docker-compose.yml` is). Do you recognize the Mongo logs? Close the cluster with `CTRL+C`, and destroy it with `docker-compose down`. A `docker ps -a` should show no containers remaining.
    - Let's add some code into `server/app.py` to push data into Mongo. You know how to do this right :D ? So create a new `GET` method so that if you connect to `/add/mango` it adds `{fruit: mango}` to mongodb, and another `GET` method `/list` that returns all fruits in mongodb.
        - Use [the Path params doc](https://fastapi.tiangolo.com/tutorial/path-params/) to get started
        - Don't forget to install pymongo both in your local environment and Dockerfile. And don't forget to rebuild your image.
        - When using `docker-compose`, the URL to connect to with your `MongoClient` is not `localhost` but `mongo`...the name of the service in the `docker-compose` file!
        - Remember, ALWAYs return Python dictionaries in FastAPI. Not only strings. Wrap up your results in `{"data": res}` if needed.

    ??? abstract "Solution ONLY if you feel stuck"
        My `server/app.py` content:
        ```python
        from fastapi import FastAPI
        from pymongo import MongoClient

        app = FastAPI()
        client = MongoClient('mongo', 27017)
        db = client.test_database
        collection = db.test_collection


        @app.get("/")
        async def root():
            return {"message": "Hello World"}

        @app.get("/add/{fruit}")
        async def add(fruit: str):
            id = collection.insert_one({"fruit": fruit}).inserted_id 
            return {"id": str(id)}

        @app.get("/list")
        async def list():
            return {"results": list(collection.find())}
        ```

!!! danger "Challenge"
    - Build a Streamlit or Gradio or Dash or Whatever app in `client/app.py` with a text input and a button to request the `http://server:8000/add/<fruit>` and then a list of all fruits currently Mongo by hitting `http://server:8000/list`. Add the correct `client/Dockerfile`, build it as `mlops:client` and add the correct information to `docker-compose.yml`.
        - If all is well, in your 3-tier architecture, Streamlit/Gradio/Dash/... is only hitting FastAPI and only FastAPI is hitting MongoDB. That way you can add authentication or security measures at FastAPI level, which would be harder to do if the client immediately hit MongoDB.

## 2. A full-stack Dockerized ML project


## 3. Adding MLFlow

docker pull ghcr.io/mlflow/mlflow
docker run -it --rm -p 5000:5000 ghcr.io/mlflow/mlflow bash
mlflow ui -h 0.0.0.0
mlflow server -h 0.0.0.0 --backend-store-uri sqlite:///mydb.sqlite

## 4. Adding Prefect