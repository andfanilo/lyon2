# TD 0 - Tooling

For this tutorial, you will be installing and configuring tools used in the following tutorials:

- Command line
- Git
- uv, to manage Python versions, environments and tools
- Docker
- An AI coding assistant in the terminal: GitHub Copilot CLI, Gemini CLI or Claude Code
- Python librairies: Streamlit & FastAPI


![](./images/prerequisites-cover.jpg)

## Objectives

- [ ] Get used to using your command prompt
- [ ] Clone a project with Git, edit it, and undo your edits
- [ ] Create a uv project with Python 3.12, FastAPI and Streamlit
- [ ] Run Python tools without installing them, with `uvx`
- [ ] Run containers and a docker compose project from the command line
- [ ] Ask an AI coding assistant to explain, edit and use a project
- [ ] Git clone the Spark tutorial

Put all the projects of these tutorials in a single workspace folder. The tutorials use `C:\workspace` on Windows and `~/workspace` on macOS and Linux. You can choose another folder: then replace `C:\workspace` with your folder in the commands.

Choose a short path without spaces, because spaces in paths cause many problems with Python, Docker and Java tools.

---

## 1. Test your command line skills

!!! warning "Try to do this without ChatGPT"
    Those are skills you will want ingrained in your brain for the rest of your developer career :smile:

!!! note "Exercise - Getting used to the Windows Prompt"
    1. Open Command Prompt from the Start Menu. On Windows 11, it opens in Windows Terminal: you can also open Windows Terminal and select **Command Prompt** from the tab dropdown.
        - On macOS or Linux, open your Terminal app instead.
    2. Open your Explorer.
    3. Select a random folder that has files in your Explorer, and browse to this folder from the Command Prompt
        - You can either use multiple `cd` commands, by pressing `tab` to autocomplete the folder to browse into. You can also copy-paste the full link from the Explorer into the command line.
    4. List all files in the folder in your Command Prompt.

The Windows and Unix command line terminals have different commands. 

Most of the following exercises use **Git Bash**, a Unix terminal for Windows that comes with Git. PowerShell, WSL, macOS, and Linux work too. When a command differs between terminals, the exercise shows it in tabs, such as `Git Bash`, `PowerShell` and `WSL / macOS / Linux`. Select the tab that matches your terminal.

!!! note "Exercise - Install Git and Git Bash"
    1. Install [Git for Windows](https://git-scm.com/downloads/win). Keep the default options. They also install Git Bash.
        - On macOS or Linux, Git is usually already installed. Check with `git --version`.
    2. Open Git Bash from the Start Menu.
    3. Run `git --version`, then browse to the same folder as in the previous exercise. Some commands differ from the Windows prompt, for example `ls` instead of `dir`, and `/` instead of `\` in paths.

!!! note "Exercise - Create your workspace"
    1. Create the `C:\workspace` folder and browse into it:

        === "Git Bash"

            ```bash
            mkdir -p /c/workspace
            cd /c/workspace
            ```

            Git Bash writes the `C:` drive as `/c`.

        === "PowerShell"

            ```powershell
            mkdir C:\workspace
            cd C:\workspace
            ```

        === "WSL / macOS / Linux"

            ```bash
            mkdir -p ~/workspace
            cd ~/workspace
            ```

            In the rest of the tutorials, replace `C:\workspace` with `~/workspace`.

    2. Run `pwd` to print the current folder. 
    3. Run `cd ..`, then `cd -`. Where are you after each command?
    4. Run `code .` to open the current folder in [VS Code](https://code.visualstudio.com/). Install VS Code if the command is not found.

---

## 2. Clone and edit a project with Git

[Git](https://git-scm.com/) records the history of a project as a list of **commits**. Each commit is a snapshot of the files, with a message that explains the change. You can always go back to an earlier snapshot.

### a. Clone a project

!!! note "Exercise - Configure Git"
    Git writes your name and email in each commit. Configure them once:

    ```bash
    git config --global user.name "Firstname Lastname"
    git config --global user.email "firstname.lastname@univ-lyon2.fr"
    ```

    Check the result with `git config --global --list`.

!!! note "Exercise - Git clone the demo project"
    1. From `C:\workspace`, download the demo project and its full history:

        ```bash
        git clone https://github.com/andfanilo/lyon2-docker-demo
        cd lyon2-docker-demo
        ```

    2. Open the folder in VS Code with `code .`. The project contains 3 Python applications:

        ```
        lyon2-docker-demo
        ├── td/                  <- A Hello World script
        ├── client/              <- A Streamlit frontend
        ├── server/              <- A FastAPI backend
        └── docker-compose.yml   <- Runs client + server + MongoDB together
        ```

    3. Run `git log --oneline`. What does each line contain? Which commit is the most recent?
    4. Run `git status`. What does `nothing to commit, working tree clean` mean?

### b. Edit the code, then undo your edits

!!! note "Exercise - Edit, restore, commit, revert"
    1. In VS Code, open `td/app.py` and replace `Hello` with `Bonjour`. Save the file.
    2. Run `git status`, then `git diff`. 
        - `git diff` shows each changed line: red lines are removed, green lines are added.
    3. You don't like your edit. Throw it away with `git restore td/app.py`, then open `td/app.py` again. 
    4. Redo the edit, then save it in a new commit:

        ```bash
        git add td/app.py
        git commit -m "Say Bonjour"
        git log --oneline
        ```

    5. You will undo the commit with `git revert --no-edit HEAD`. Before you run it, predict: after the revert, will your `Say Bonjour` commit still be in `git log --oneline`? What will `td/app.py` contain?
        - `HEAD` is the latest commit. `--no-edit` keeps the default commit message, `Revert "Say Bonjour"`, instead of opening an editor.
    6. Run the revert, then `git log --oneline` and open `td/app.py`. Was your prediction right?

!!! question
    - When should you use `git restore`, and when should you use `git revert`?
    - Why does `git revert` add a new commit, instead of deleting the old one?

You can't `git push` your commits to this project: it belongs to someone else. You will push to your own GitHub repositories in later tutorials.

??? tip "Going further"
    - Run `git log -p`. It shows the diff of each commit. Press `q` to quit.
    - Run `git show HEAD~1`. Which commit is `HEAD~1`?
    - Create a branch with `git switch -c my-test`, commit an edit on it, then go back with `git switch -`. Is your edit still in `td/app.py`? Run `git log --oneline --all --graph` to see both branches.
        - Older tutorials use `git checkout -b my-test` and `git checkout -`. They do the same thing: `git switch` and `git restore` replace the two jobs of `git checkout`.

---

## 3. Create a complete Python environment

Each project needs its own Python version and its own packages. If all your projects share one installation, upgrading a package for one project can break another.

[uv](https://docs.astral.sh/uv/) manages both for you. It installs Python versions, creates isolated environments, installs packages, and runs Python tools. It is also very fast :rocket:

### a. Install uv and Python

!!! note "Exercise - Installing uv"
    1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/):

        === "Git Bash / PowerShell"

            ```bash
            powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
            ```

        === "WSL / macOS / Linux"

            ```bash
            curl -LsSf https://astral.sh/uv/install.sh | sh
            ```

    2. Close and reopen your terminal, then run `uv --version`. If the command is not found, check the end of the installer output: it tells you which folder to add to your `PATH`.
    3. Install Python 3.12 with `uv python install 3.12`. You don't need to download Python from python.org: uv manages Python versions for you.
    4. List the Python versions uv knows about with `uv python list`. Which ones are installed?

### b. Create a uv project

A **uv project** records its dependencies in a `pyproject.toml` file, and the exact installed versions in a `uv.lock` file. uv installs them in a **virtual environment**: a `.venv` folder inside the project, with its own Python and its own packages. Anyone with `pyproject.toml` and `uv.lock` can recreate exactly the same environment.

!!! note "Exercise - Create a uv project"
    1. Go back to `C:\workspace`, then create a new project: `uv init uv-project-td --app --no-package --python 3.12`. Browse into `uv-project-td`.
        - `--app --no-package` creates an application with a single `main.py` script, instead of a Python package to publish.
    2. Open the folder in your editor. What does each of `pyproject.toml`, `.python-version` and `main.py` contain?
    3. Add FastAPI and Streamlit to the project: `uv add fastapi streamlit`.
        - What changed in `pyproject.toml`?
        - What new files and folders appeared? Open `uv.lock` and search for `streamlit`.
    4. Run commands inside the project environment with `uv run`. You don't need to activate the environment:

        a. `uv run python --version`. Before you run it, predict which version it prints, and why. Compare with `python --version`, if Python is installed on your machine.

        b. `uv run main.py`. You should see `Hello from uv-project-td!`

        c. `uv run streamlit version`

        d. `uv run python -m http.server`, then open <http://localhost:8000>. Stop the server with `Ctrl+C`.

    5. Delete the `.venv` folder, then run `uv sync`. What happened? What does `uv sync` do when a classmate clones your project?
    6. Remove a dependency with `uv remove fastapi`, then check `pyproject.toml` again. Add it back with `uv add fastapi`.

!!! question
    - You send the `uv-project-td` folder to a classmate without its `.venv`. Which command recreates your environment?
    - Why should you commit `pyproject.toml` and `uv.lock` to Git, but never `.venv`?

### c. Run the demo project with uv

Each of the `td`, `client` and `server` folders of `lyon2-docker-demo` is its own uv project, with its own `pyproject.toml` and `uv.lock`. You don't install anything by hand: `uv run` creates the `.venv` and installs the locked packages the first time.

!!! note "Exercise - Run the 3 applications locally"
    1. Browse into `C:\workspace\lyon2-docker-demo\td`. Open `pyproject.toml`: which package does the script need?
        - Run the script with your own Python first: `python app.py`. Read the error. Why does it fail?
        - Now run it with `uv run app.py`. Why does it work this time?
    2. Browse into `../server`. Start the FastAPI server: `uv run uvicorn --reload app:app`. 
        - Open <http://localhost:8000> and <http://localhost:8000/docs>. 
        - With `--reload`, the server restarts when you save a file. Edit the `Hello World` message in `server/app.py`, save, then refresh the page.
        - Stop the server with `Ctrl+C`. Then throw your edit away with Git.
    3. Browse into `../client`. Start the Streamlit app: `uv run streamlit run streamlit_app.py`, then open <http://localhost:8501>. 
        - Press `Predict flower`. Why does it fail? Look at the URL in `streamlit_app.py`: the `server` name only exists inside docker compose. You fix this in the next section.
        - Stop the app with `Ctrl+C`.

!!! question
    - The `client` and `server` folders each have a `.venv`. Why not share one environment for the whole repository?
    - Run `git status` from `lyon2-docker-demo`. Why doesn't Git list the new `.venv` folders? Open `.gitignore`.

### d. Run Python tools with uvx

Some Python packages are **tools** you run from the command line, like Jupyter or the [Ruff](https://docs.astral.sh/ruff/) linter. They don't need to be part of your project.

!!! note "Exercise - Tools with uvx and uv tool"
    1. Run `uvx ruff --version`. `uvx` downloads Ruff into a temporary, isolated environment and runs it.
    2. From the `uv-project-td` folder, check the code of `main.py` with `uvx ruff check`. You should see `All checks passed!`. Did `pyproject.toml` change?
        - Ruff is a **linter**: it reads your code without running it, and reports bugs and bad practices.
    3. Break the code. Replace the content of `main.py` with:

        ```python
        import os


        def main():
            message = "Hello from uv-project-td!"
            print(mesage)


        if __name__ == "__main__":
            main()
        ```

        - Run `uv run main.py`. Which error do you get?
        - Run `uvx ruff check`. Ruff finds the same bug without running the code. You made one typo: why does Ruff report two errors about it?
        - Run `uvx ruff check --fix`. Which error does Ruff fix by itself? Fix the other errors yourself, then run `uvx ruff check` until you see `All checks passed!`.
    4. Ruff is also a **formatter**: it rewrites the layout of your code, without changing what it does. Add these badly formatted lines to `main.py`, just before `if __name__ == "__main__":`:

        ```python
        def add(a,b) : return a+b
        numbers=[1,2 ,3]
        ```

        - Run `uvx ruff check`. Does the linter complain?
        - Preview the changes with `uvx ruff format --diff`, then apply them with `uvx ruff format`. Open `main.py`: what changed?
    5. Run `uvx jupyter lab`. JupyterLab opens in your browser, and your project stays unchanged. Stop the server with `Ctrl+C`.
    6. Install Ruff permanently with `uv tool install ruff`. Now run `ruff --version` from any folder. List the installed tools with `uv tool list`.

!!! question
    - When should you use `uv add`, `uvx` and `uv tool install`? Give an example package for each.
    - Why would you rather `uvx` a tool than `uv add` it to your project?
    - What is the difference between a linter and a formatter? Which one caught your `mesage` typo?

??? tip "Going further"
    - In `uv-project-td`, add Ruff as a development dependency with `uv add --dev ruff`. Where does it appear in `pyproject.toml`? Run it with `uv run ruff check`.
    - Print the dependency tree with `uv tree`. Which packages did `streamlit` bring in?
    - Run a one-off command with an extra package, without adding it to the project. First run `uv run python -c "import cowsay"`: why does it fail? Then run `uv run --with cowsay python -c "import cowsay; cowsay.cow('Bonjour')"`. Did `pyproject.toml` change?

---

## 4. Run containers with Docker

[Docker](https://www.docker.com/) packages an application with everything it needs (operating system, Python, packages, code) into an **image**. A running image is a **container**. If it runs on your machine, it runs the same way on a classmate's machine or on a server.

Try your best not to use the Docker dashboard. Use the command line instead. You won't have a dashboard when manipulating Docker in production.

### a. Check your Docker installation

Depending on how Docker was installed, it may be that `docker compose` does not work correctly.

!!! note "Exercise - Testing Docker commands"
    1. Open Git Bash from the Start Menu.
    2. Test the following commands:

        a. `docker version` 

        b. `docker compose version`

        c. `docker images`

    If one of these doesn't work, especially the `docker compose version`, you probably need to uninstall and reinstall [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### b. Your first containers

!!! note "Exercise - Hello World"
    1. Download the `hello-world` image with `docker pull hello-world`, then list your images with `docker images`.
    2. Run it with `docker run hello-world`. Read the output: it explains what Docker just did.
    3. `docker ps` lists the running containers, and `docker ps -a` lists all containers. Before you run them, predict: is the `hello-world` container in the first list, the second, or both? Run them and explain the result.
    4. Delete the stopped container with `docker rm <container id>`. You only need to type the first characters of the ID.

!!! note "Exercise - Run Python code in a container"
    The [python](https://hub.docker.com/_/python) image on [Docker Hub](https://hub.docker.com/) contains Linux and Python. You can run Python code without installing Python.

    1. Download the image: `docker pull python:3.12-slim`. 
        - `python` is the image name, `3.12-slim` is the **tag**: a version of the image. Browse the other tags on Docker Hub.
    2. Run one Python command in a new container. You should see `5`:

        ```bash
        docker run --rm python:3.12-slim python -c "print(2 + 3)"
        ```

        - `--rm` deletes the container when it stops. Check with `docker ps -a`.
    3. Open an interactive Python shell in a container: `docker run -it --rm python:3.12-slim python`. 
        - `-it` connects your keyboard and terminal to the container. 
        - Run `import platform; platform.platform()`. Which operating system runs your code? Quit with `exit()`.

!!! note "Exercise - Run commands in a background container"
    1. Start a container in the background, and run commands inside it with `docker exec`:

        ```bash
        docker run -d --name py-demo python:3.12-slim sleep infinity
        docker ps
        docker exec py-demo python -c "import sys; print(sys.version)"
        docker exec -it py-demo bash
        ```

        - `-d` runs the container in the background, `--name` gives it a name instead of an ID.
        - `sleep infinity` keeps the container running, so you can `exec` into it.
        - `docker exec -it py-demo bash` opens a shell inside the container. Run `ls /` and `pwd`, then `exit`.
    2. Stop and delete the container: `docker rm -f py-demo`.

!!! question
    - What is the difference between `docker run` and `docker exec`?
    - What is the difference between an image and a container?

### c. Build and run the demo project

!!! note "Exercise - Build your first image"
    1. Open `C:\workspace\lyon2-docker-demo\td\Dockerfile`:

        ```Dockerfile
        FROM python:3.12-slim
        COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

        WORKDIR /app
        COPY pyproject.toml uv.lock /app/
        RUN uv sync --locked --no-install-project

        COPY app.py app.py

        CMD ["uv", "run", "app.py"]
        ```

        - The image starts from `python:3.12-slim`, copies the `uv` program in, installs the packages of `uv.lock`, copies the code, and runs it with `uv run`. You write such Dockerfiles yourself in the [MLOps tutorial](mlops.md).
    2. From the `td` folder, build an image named `td-lyon2` with `docker build`. Search `docker build --help` for the option that names an image.
    3. Run your image in a container that is deleted when it stops. Compare its output with `uv run app.py`.

    ??? tip "Hint"
        ```bash
        docker build -t td-lyon2 .
        docker run --rm td-lyon2
        ```

        `-t` names the image. `.` is the folder that contains the `Dockerfile`.

!!! note "Exercise - Run the full application with docker compose"
    1. Open `docker-compose.yml`. Which 3 services does it start? Which ports does it expose?
    2. From the `lyon2-docker-demo` folder, build and start everything: `docker compose up --build`. 
    3. Open <http://localhost:8501>, move some sliders and press `Predict flower`. This time, the client reaches the server and displays an answer: docker compose gives each service a network name, like `server`.
    4. Open <http://localhost:8000/add/banana>, then <http://localhost:8000/list>. The server stored your fruit in the MongoDB container.
    5. From a second terminal, run a command inside the running `server` container:

        ```bash
        docker compose exec server uv run python -c "import sys; print(sys.version)"
        ```

    6. Stop everything with `Ctrl+C` in the first terminal, then delete the containers with `docker compose down`.
    7. Predict: if you start the application again and open <http://localhost:8000/list>, is your `banana` still there? Check with `docker compose up -d`, then stop with `docker compose down`.

!!! question
    - Your local Python and the container's Python may have different versions. Why does the application still work the same?
    - Why don't you need to install MongoDB on your machine?
    - Where did MongoDB store your `banana`? Why did `docker compose down` lose it?

??? tip "Going further"
    - Follow the logs of one service while you use the app: `docker compose logs -f server`.
    - Keep MongoDB data across `docker compose down` with a **named volume**. In `docker-compose.yml`:

        ```yaml
        services:
          mongo:
            image: mongo
            volumes:
              - mongo-data:/data/db
        # ... client and server unchanged ...

        volumes:
          mongo-data:
        ```

        Add a fruit, run `docker compose down` then `docker compose up -d`. Is it still there? `docker compose down -v` deletes the volume too. Throw the edit away with Git afterwards.
    - How much disk space do your images and containers use? Run `docker system df`.

---

## 5. Work with an AI coding assistant

An AI coding assistant in the terminal reads your project, edits files and runs commands. Before each edit or command, it asks for your permission: read what it wants to do before you accept.

Pick one assistant. [GitHub Copilot](https://github.com/education/students) and [Gemini CLI](https://github.com/google-gemini/gemini-cli) have free plans for students. [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) needs a paid Claude plan.

!!! note "Exercise - Install an AI coding assistant"
    1. Install the assistant, then start it from the `lyon2-docker-demo` folder:

        === "GitHub Copilot CLI"

            Install [Node.js](https://nodejs.org/) LTS first, then:

            ```bash
            npm install -g @github/copilot
            cd /c/workspace/lyon2-docker-demo
            copilot
            ```

            Type `/login` and sign in with your GitHub account.

        === "Gemini CLI"

            Install [Node.js](https://nodejs.org/) LTS first, then:

            ```bash
            npm install -g @google/gemini-cli
            cd /c/workspace/lyon2-docker-demo
            gemini
            ```

            Choose `Login with Google` and sign in with your Google account.

        === "Claude Code"

            In PowerShell, or with `curl -fsSL https://claude.ai/install.sh | bash` in WSL, macOS or Linux:

            ```powershell
            irm https://claude.ai/install.ps1 | iex
            ```

            Then, from Git Bash:

            ```bash
            cd /c/workspace/lyon2-docker-demo
            claude
            ```

            Sign in with your Claude account.

    2. Quit the assistant with `/exit` or `Ctrl+C` twice.

!!! note "Exercise - Explain, edit, review"
    1. Ask the assistant to explain the project:

        ```text
        Explain the architecture of this project and how client, server and MongoDB talk to each other
        ```

        Compare its answer with what you discovered in the previous sections.

    2. Ask for a code change:

        ```text
        Add a GET /health endpoint to server/app.py that returns {"status": "ok"}, then run the server with uv and test it
        ```

        Accept or refuse each edit and command it asks for. Which commands did it run?

    3. Don't trust the assistant's summary: test its work yourself. If the server stopped, start it from the `server` folder with `uv run uvicorn app:app`. Open <http://localhost:8000/health>: you should see `{"status":"ok"}`.
    4. Review its work like a colleague's work, from a second terminal: `git status` and `git diff`. Keep the edit with a commit, or throw it away with `git restore .`

### Let the assistant use the Streamlit app

Streamlit has an **agent API**: when you turn it on, the app also serves an [MCP](https://modelcontextprotocol.io/) server at `/_stcore/agent/mcp`. Through MCP, an assistant fills the form and presses buttons like a browser user would, without a browser.

!!! note "Exercise - Connect the assistant to the app with MCP"
    1. Ask the assistant to turn the agent API on:

        ```text
        In docker-compose.yml, enable Streamlit's agent API on the client service with the STREAMLIT_SERVER_ENABLE_AGENT_API environment variable
        ```

        Check the edit with `git diff`. Streamlit reads every `STREAMLIT_*` environment variable as a configuration option.

    2. Quit the assistant. Start the application in the background with `docker compose up --build -d`, so you get your terminal back.
    3. Register the app's MCP server in your assistant, under the name `iris-app`:

        === "GitHub Copilot CLI"

            ```bash
            copilot mcp add --transport http iris-app http://localhost:8501/_stcore/agent/mcp
            ```

        === "Gemini CLI"

            ```bash
            gemini mcp add --transport http iris-app http://localhost:8501/_stcore/agent/mcp
            ```

        === "Claude Code"

            ```bash
            claude mcp add --transport http iris-app http://localhost:8501/_stcore/agent/mcp
            ```

    4. Start the assistant again. Run `/mcp` to check that `iris-app` is connected, then ask:

        ```text
        Use the iris-app MCP server: set sepal length 5, sepal width 3, petal length 1, petal width 0, press Predict flower and tell me what the app displays
        ```

        The assistant should tell you what the app writes under the form after the button press. Compare with what you saw in your browser in the previous section.

        Run `docker compose logs server`. Can you find the request the app sent to the server when the assistant pressed the button? Look for a line with `POST /predict`.

    5. Stop the application with `docker compose down`.

!!! question
    - The app answers with the numbers you sent, not with a flower name. Why? Read `server/app.py` and `server/train.py`.
    - An assistant connected to an app over MCP can do anything a user of the app can do. Which apps would you not connect an assistant to?

??? tip "Going further"
    - Ask the assistant to write a test for the `/health` endpoint with `pytest`, add `pytest` as a development dependency with uv, and run the test. Read the test: does it check what you expect?
    - Ask the assistant to add a named volume to MongoDB, as in the Docker **Going further** block. Check its edit with `git diff` before you accept it.

---

## 6. Git clone a Jupyter project

!!! note "Exercise - Git cloning a project"
    1. Open Git Bash from the Start Menu.
    2. Browse into `C:\workspace`.
    3. Clone the spark tutorial on https://github.com/andfanilo/pyspark-tutorial to your folder
    4. Follow the [Spark tutorial setup](spark.md#1-install-the-tutorial): install Java, run `uv sync`, then open the notebooks in JupyterLab or VS Code. Make sure you can run the Spark setup cell of `2-novice/1-Initiation-RDD.ipynb`.

---

## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Get used to using your command prompt
    - [x] Clone a project with Git, edit it, and undo your edits
    - [x] Create a uv project with Python 3.12, FastAPI and Streamlit
    - [x] Run Python tools without installing them, with `uvx`
    - [x] Run containers and a docker compose project from the command line
    - [x] Ask an AI coding assistant to explain, edit and use a project
    - [x] Git clone the Spark tutorial

Take note of those tools. You will use them throughout the tutorials.

In the next tutorial, we will delve into dockerizing a ML Prediction service with FastAPI and Streamlit.
