# TD0 - Tooling

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

All the projects of these tutorials go into a single `C:\workspace` folder. Short paths without spaces avoid many problems with Python, Docker and Java tools.

---

## 1. Test your command line skills

!!! warning "Try to do this without ChatGPT"
    Those are skills you will want ingrained in your brain for the rest of your developer career :smile:

!!! note "Exercise - Getting used to the Windows Prompt"
    1. Open your Command Prompt Terminal from the Start Menu.
    2. Open your Explorer.
    3. Select a random folder that has files in your Explorer, and browse to this folder from the Command Prompt
        - You can either use multiple `cd` commands, by pressing `tab` to autocomplete the folder to browse into. You can also copy-paste the full link from the Explorer into the command line.
    4. List all files in the folder in your Command Prompt.

The Windows and Unix command line terminals have different commands. 

Most of the following exercises use **Git Bash**, a Unix terminal for Windows that comes with Git. PowerShell, WSL, macOS, and Linux work too. When a command differs between terminals, each terminal gets its own tab.

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

    5. Undo the commit with `git revert --no-edit HEAD`. 
        - `HEAD` is the latest commit. `--no-edit` keeps the default commit message, `Revert "Say Bonjour"`, instead of opening an editor.
    6. Run `git log --oneline` again. Is your `Say Bonjour` commit still in the history?

!!! question
    - When should you use `git restore`, and when should you use `git revert`?
    - Why does `git revert` add a new commit, instead of deleting the old one?

You can't `git push` your commits to this project: it belongs to someone else. You will push to your own GitHub repositories in later tutorials.

---

## 3. Create a complete Python environment

Each project needs its own Python version and its own packages. If all your projects share one installation, upgrading a package for one project can break another.

[uv](https://docs.astral.sh/uv/) manages both for you. It installs Python versions, creates isolated environments, installs packages, and runs Python tools. It is also very fast :rocket:

### a. Install uv and Python

!!! note "Exercise - Installing uv"
    1. Install uv:

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

        a. `uv run python --version`. Compare with `python --version`, if Python is installed on your machine.

        b. `uv run main.py`

        c. `uv run streamlit version`

        d. `uv run python -m http.server`, then open <http://localhost:8000>. Stop the server with `Ctrl+C`.

    5. Delete the `.venv` folder, then run `uv sync`. What happened? A classmate runs `uv sync` after cloning your project.
    6. Remove a dependency with `uv remove fastapi`, then check `pyproject.toml` again.

!!! question
    - You send the `uv-project-td` folder to a classmate without its `.venv`. Which command recreates your environment?
    - Why should you commit `pyproject.toml` and `uv.lock` to Git, but never `.venv`?

### c. Run the demo project with uv

Each of the `td`, `client` and `server` folders of `lyon2-docker-demo` is its own uv project, with its own `pyproject.toml` and `uv.lock`. You don't install anything by hand: `uv run` creates the `.venv` and installs the locked packages the first time.

!!! note "Exercise - Run the 3 applications locally"
    1. Browse into `C:\workspace\lyon2-docker-demo\td`. Open `pyproject.toml`: which package does the script need? Run the script with `uv run app.py`. 
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
    2. From the `uv-project-td` folder, check the code of `main.py` with `uvx ruff check`. Did `pyproject.toml` change?
    3. Run `uvx jupyter lab`. JupyterLab opens in your browser, and your project stays unchanged. Stop the server with `Ctrl+C`.
    4. Install Ruff permanently with `uv tool install ruff`. Now run `ruff --version` from any folder. List the installed tools with `uv tool list`.

!!! question
    - When should you use `uv add`, `uvx` and `uv tool install`? Give an example package for each.
    - Why would you rather `uvx` a tool than `uv add` it to your project?

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
    3. List the running containers with `docker ps`, then all containers with `docker ps -a`. Why is the `hello-world` container in the second list only?
    4. Delete the stopped container with `docker rm <container id>`. You only need to type the first characters of the ID.

!!! note "Exercise - Run Python code in a container"
    The [python](https://hub.docker.com/_/python) image on [Docker Hub](https://hub.docker.com/) contains Linux and Python. You can run Python code without installing Python.

    1. Download the image: `docker pull python:3.12-slim`. 
        - `python` is the image name, `3.12-slim` is the **tag**: a version of the image. Browse the other tags on Docker Hub.
    2. Run one Python command in a new container: 

        ```bash
        docker run --rm python:3.12-slim python -c "print(2 + 3)"
        ```

        - `--rm` deletes the container when it stops. Check with `docker ps -a`.
    3. Open an interactive Python shell in a container: `docker run -it --rm python:3.12-slim python`. 
        - `-it` connects your keyboard and terminal to the container. 
        - Run `import platform; platform.platform()`. Which operating system runs your code? Quit with `exit()`.
    4. Start a container in the background, and run commands inside it with `docker exec`:

        ```bash
        docker run -d --name py-demo python:3.12-slim sleep infinity
        docker ps
        docker exec py-demo python -c "import sys; print(sys.version)"
        docker exec -it py-demo bash
        ```

        - `-d` runs the container in the background, `--name` gives it a name instead of an ID.
        - `sleep infinity` keeps the container running, so you can `exec` into it.
        - `docker exec -it py-demo bash` opens a shell inside the container. Run `ls /` and `pwd`, then `exit`.
    5. Stop and delete the container: `docker rm -f py-demo`.

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
    2. From the `td` folder, build the image with `docker build -t td-lyon2 .`
        - `-t` names the image. `.` is the folder that contains the `Dockerfile`.
    3. Run it with `docker run --rm td-lyon2`. Compare with the output of `uv run app.py`.

!!! note "Exercise - Run the full application with docker compose"
    1. Open `docker-compose.yml`. Which 3 services does it start? Which ports does it expose?
    2. From the `lyon2-docker-demo` folder, build and start everything: `docker compose up --build`. 
    3. Open <http://localhost:8501>, move some sliders and press `Predict flower`. This time, the client reaches the server: docker compose gives each service a network name, like `server`.
    4. Open <http://localhost:8000/add/banana>, then <http://localhost:8000/list>. The server stored your fruit in the MongoDB container.
    5. From a second terminal, run a command inside the running `server` container:

        ```bash
        docker compose exec server uv run python -c "import sys; print(sys.version)"
        ```

    6. Stop everything with `Ctrl+C` in the first terminal, then delete the containers with `docker compose down`.

!!! question
    - Your local Python and the container's Python may have different versions. Why does the application still work the same?
    - Why don't you need to install MongoDB on your machine?

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

    3. Review its work like a colleague's work, from a second terminal: `git status` and `git diff`. Keep the edit with a commit, or throw it away with `git restore .`

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

        Run `docker compose logs server`. Can you find the request the app sent to the server when the assistant pressed the button?

    5. Stop the application with `docker compose down`.

!!! question
    - The app answers with the numbers you sent, not with a flower name. Why? Read `server/app.py` and `server/train.py`.
    - An assistant connected to an app over MCP can do anything a user of the app can do. Which apps would you not connect an assistant to?

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
