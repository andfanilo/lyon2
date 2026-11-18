# TD0 - Tooling

For this tutorial, you will be installing and configuring tools used in the following tutorials:

- Command line
- Git
- uv, to manage Python versions, environments and tools
- Docker
- Python librairies: Streamlit & FastAPI


![](./images/prerequisites-cover.jpg)

## Objectives

- [ ] Get used to using your command prompt
- [ ] Create a uv project with Python 3.12, FastAPI and Streamlit
- [ ] Run Python tools without installing them, with `uvx`
- [ ] Reinstall Docker to ensure a clean docker-compose environment
- [ ] Git clone the NoSQL or Spark tutorial

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

---

## 2. Create a complete Python environment

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

### b. Create a virtual environment by hand

A **virtual environment** is a folder, usually named `.venv`, that contains its own Python and its own packages. First, create one by hand.

!!! note "Exercise - Create and activate a virtual environment"
    1. Create a new folder `uv-venv-td` and browse into it.
    2. Create a virtual environment with Python 3.12: `uv venv --python 3.12`. What new folder appeared?
    3. **Activate** the environment, so that the `python` command and the installed packages come from `.venv`:

        === "Git Bash"

            ```bash
            source .venv/Scripts/activate
            ```

        === "PowerShell"

            ```powershell
            .venv\Scripts\activate
            ```

            If PowerShell refuses to run the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then retry.

        === "WSL / macOS / Linux"

            ```bash
            source .venv/bin/activate
            ```

        When activated, how do you know you're in the correct environment?

    4. To ensure Python is properly installed:

        a. Run `python --version` to check the Python version

        b. Run `python -m http.server` to have Python run an HTTP server on `http://localhost:8000`. Stop it with `Ctrl+C`.

    5. In the activated environment, install packages with `uv pip install fastapi streamlit`. Run `streamlit version` to check that it works.
    6. Run `deactivate` to leave the environment. Does `streamlit version` still work?

This works, but nothing records which packages you installed. A classmate who clones your code has to guess what to install.

### c. Record dependencies in a uv project

A **uv project** records its dependencies in a `pyproject.toml` file, and the exact installed versions in a `uv.lock` file. Anyone with these 2 files can recreate exactly the same environment.

!!! note "Exercise - Create a uv project"
    1. Go back to your folder of projects, then create a new project: `uv init uv-project-td --app --no-package --python 3.12`. Browse into `uv-project-td`.
        - `--app --no-package` creates an application with a single `main.py` script, instead of a Python package to publish.
    2. Open the folder in your editor. What does each of `pyproject.toml`, `.python-version` and `main.py` contain?
    3. Add FastAPI and Streamlit to the project: `uv add fastapi streamlit`.
        - What changed in `pyproject.toml`?
        - What new files and folders appeared? Open `uv.lock` and search for `streamlit`.
    4. Run commands inside the project environment with `uv run`, **without activating anything**:

        a. `uv run python --version`

        b. `uv run main.py`

        c. `uv run streamlit version`

    5. Delete the `.venv` folder, then run `uv sync`. What happened? A classmate runs `uv sync` after cloning your project.
    6. Remove a dependency with `uv remove fastapi`, then check `pyproject.toml` again.

!!! question
    - Compare the `uv-venv-td` and `uv-project-td` folders. If you send each folder to a classmate without its `.venv`, how do they recreate your environment?
    - Why should you commit `pyproject.toml` and `uv.lock` to Git, but never `.venv`?

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

## 3. Repair your Docker environment

Depending on how Docker was installed, it may be that `docker compose` does not work correctly.

Try your best not to use the Docker dashboard. Use the command line instead. You won't have a dashboard when manipulating Docker in production.

!!! note "Exercise - Testing Docker commands"
    1. Open Git Bash from the Start Menu.
    2. Test the following commands:

        a. `docker version` 

        b. `docker compose version`

        c. `docker images`

        d. `docker pull hello-world`

        e. `docker run hello-world`

        f. `docker ps -a`

    If one of these doesn't work, especially the `docker compose version`, you probably need to uninstall and reinstall [Docker Desktop](https://www.docker.com/products/docker-desktop/).

---

## 4. Git clone a Jupyter project

!!! note "Exercise - Git cloning a project"
    1. Open Git Bash from the Start Menu.
    2. Browse into your folder of choice for new projects.
    3. Clone the spark tutorial on https://github.com/andfanilo/pyspark-tutorial to your folder
    4. Follow the [Spark tutorial setup](spark.md#1-install-the-tutorial): install Java, run `uv sync`, then open the notebooks in JupyterLab or VS Code. Make sure you can run the Spark setup cell of `2-novice/1-Initiation-RDD.ipynb`.

---

## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Get used to using your command prompt
    - [x] Create a uv project with Python 3.12, FastAPI and Streamlit
    - [x] Run Python tools without installing them, with `uvx`
    - [x] Reinstall Docker to ensure a clean docker-compose environment
    - [x] Git clone the Spark tutorial

Take note of those tools. You will use them throughout the tutorials.

In the next tutorial, we will delve into dockerizing a ML Prediction service with FastAPI and Streamlit.
