# TD3 - Introduction to Spark

Link to tutorial: <https://github.com/andfanilo/pyspark-tutorial>

![](./images/spark-cover.jpg)

## Objectives

- [ ] Install Java and the Spark tutorial environment with uv
- [ ] Configure the environment variables Spark needs
- [ ] Run a Spark notebook from JupyterLab or VS Code

---

## 1. Install the tutorial

Spark runs on the Java Virtual Machine (JVM). PySpark is the Python library that drives it. You need both Java and a Python environment.

!!! note "Exercise - Install Java"
    1. Install a Java JDK, version **17 or 21**, for example [Eclipse Temurin](https://adoptium.net/). Other Java versions may not work with Spark.
        - On Windows, in the installer, enable **Set JAVA_HOME variable**. It saves you the next step.
    2. Check that the `JAVA_HOME` environment variable points to the JDK folder, the one that contains `bin/java`:

        === "Git Bash"

            ```bash
            echo $JAVA_HOME
            "$JAVA_HOME/bin/java" -version
            ```

        === "PowerShell"

            ```powershell
            echo $env:JAVA_HOME
            & "$env:JAVA_HOME\bin\java" -version
            ```

        === "WSL / macOS / Linux"

            ```bash
            echo $JAVA_HOME
            "$JAVA_HOME/bin/java" -version
            ```

    3. If `JAVA_HOME` is empty, set it **permanently**, so that every terminal and every editor sees it:
        - On Windows, search for **Edit environment variables for your account** in the Start Menu. Add a variable `JAVA_HOME` with the JDK folder, for example `C:\Program Files\Eclipse Adoptium\jdk-21.0.5.11-hotspot`.
        - On macOS or Linux, add `export JAVA_HOME=<path_to_jdk>` to your `~/.bashrc` or `~/.zshrc`.
    4. **Close all your terminals and all VS Code windows**, then reopen them and check again. A program only reads environment variables when it starts.

!!! note "Exercise - Install the Python environment"
    1. Clone the tutorial: `git clone https://github.com/andfanilo/pyspark-tutorial`, then browse into the `pyspark-tutorial` folder.
    2. Run `uv sync`. uv downloads Python 3.10 and installs PySpark, Jupyter and the other dependencies into a `.venv` folder.
        - The project is pinned to Python 3.10 on purpose: on Windows, PySpark crashes on Python 3.11 and above for some RDD operations. Don't change the pin.

---

## 2. Configure the environment variables

Spark needs 2 environment variables:

| Variable | What it does | Where to set it |
| --- | --- | --- |
| `JAVA_HOME` | Tells PySpark which JVM to start. | Once for your account. You did it in the previous section. |
| `PYSPARK_PYTHON` | Tells Spark which Python command to run for its workers. | For each project, because each project has its own Python. |

Without `PYSPARK_PYTHON`, Spark workers may start another Python than the one in `.venv`. On Windows, Spark starts `python3` by default, which is often the Microsoft Store placeholder. Your code then fails with errors like `Python worker failed to connect back`.

!!! tip "How environment variables reach your notebook"
    The notebook kernel inherits the environment variables of the program that starts it:

    - With **JupyterLab**, that is your terminal. Set the variables in the terminal, then start JupyterLab from that same terminal.
    - With **VS Code**, that is VS Code itself, which does not see variables you set in a terminal. Use a `.env` file instead, as shown below.

---

## 3. Run the notebooks

Use **either** JupyterLab or VS Code.

### a. Option A - JupyterLab

!!! note "Exercise - Start JupyterLab"
    1. From the `pyspark-tutorial` folder, set `PYSPARK_PYTHON` and start JupyterLab **in the same terminal**:

        === "Git Bash"

            ```bash
            export PYSPARK_PYTHON=python
            uv run jupyter lab
            ```

        === "PowerShell"

            ```powershell
            $env:PYSPARK_PYTHON = "python"
            uv run jupyter lab
            ```

        === "WSL / macOS / Linux"

            ```bash
            export PYSPARK_PYTHON=python
            uv run jupyter lab
            ```

        `uv run` puts the `.venv` Python first on the `PATH`, so `python` is the project's Python.

    2. Open `1-beginner/1-Initiation.ipynb`.

    You must set the variable again every time you open a new terminal.

### b. Option B - VS Code

!!! note "Exercise - Install the VS Code extensions"
    In the Extensions view (`Ctrl+Shift+X`), install the **Python** and **Jupyter** extensions published by Microsoft.

!!! note "Exercise - Select the uv environment"
    1. Run `uv sync` **before** you open the project, so that the `.venv` folder exists.
    2. Open the folder in VS Code with **File > Open Folder...**, and select the `pyspark-tutorial` folder itself. Do not open its parent folder: VS Code only finds the `.venv` folder at the root of the folder you open.
    3. Select the Python interpreter: press `Ctrl+Shift+P`, run **Python: Select Interpreter**, and select the entry that shows `.venv`, `Python 3.10` and the path `.venv\Scripts\python.exe` (`.venv/bin/python` on macOS or Linux).
        - If it isn't in the list, select **Enter interpreter path...** and type `.venv\Scripts\python.exe` (`.venv/bin/python` on macOS or Linux).
    4. Open `1-beginner/1-Initiation.ipynb`. Select **Select Kernel** in the top right corner of the notebook, then **Python Environments...**, then the same `.venv` environment.

!!! warning "Don't let VS Code create or change the environment"
    uv manages the environment. When VS Code offers to:

    - **Create a virtual environment**: decline. Run `uv sync` instead.
    - **Install `ipykernel`**: decline. The `.venv` already contains it, so this message means you selected the wrong environment. Go back to step 3.

    Add or remove packages with `uv add` and `uv remove` only.

!!! note "Exercise - Set `PYSPARK_PYTHON` with a `.env` file"
    1. At the root of the `pyspark-tutorial` folder, next to `pyproject.toml`, create a file named `.env` with this content:

        ```bash
        PYSPARK_PYTHON=python
        ```

    2. VS Code reads the `.env` file only when it starts the kernel. Restart the kernel with the **Restart** button at the top of the notebook. If the variable is still missing, run **Developer: Reload Window** from `Ctrl+Shift+P`.

!!! tip "If the `.env` file isn't read"
    Set the variable from Python, in a new cell at the top of the notebook, **before** the cell that creates the `SparkContext` or `SparkSession`:

    ```python
    import os
    import sys

    os.environ["PYSPARK_PYTHON"] = sys.executable
    ```

    `sys.executable` is the full path of the kernel's Python, so Spark workers run the same Python as your notebook. This works in JupyterLab too. If Spark is already running, restart the kernel first.

---

## 4. Check your setup

!!! note "Exercise - Run your first Spark job"
    1. In a new cell at the top of `1-beginner/1-Initiation.ipynb`, run:

        ```python
        import os
        import sys

        print(sys.executable)
        print(os.environ.get("JAVA_HOME"))
        print(os.environ.get("PYSPARK_PYTHON"))
        ```

        - The first line must end with `.venv\Scripts\python.exe` (`.venv/bin/python` on macOS or Linux). If not, select the kernel again.
        - The second line must be your JDK folder. If it is `None`, go back to the **Install Java** exercise, and close **all** VS Code windows before you reopen VS Code.
        - The third line must be `python`, or a path to a Python executable. If it is `None`, set `PYSPARK_PYTHON` again.

    2. Run a small Spark job:

        ```python
        from pyspark import SparkContext

        sc = SparkContext.getOrCreate()
        print(sc.parallelize(range(10)).sum())
        ```

        It must print `45`. While Spark runs, open <http://localhost:4040> to see the Spark UI.

    3. Delete the 2 cells and restart the kernel, then start the tutorial.

!!! warning "Common errors"
    - `JAVA_HOME is not set` or `Java gateway process exited before sending its port number`: Spark can't find Java. Check `JAVA_HOME`, then restart your terminal or VS Code.
    - `Python worker failed to connect back` or `Python worker exited unexpectedly`: Spark started the wrong Python. Check `PYSPARK_PYTHON`.
    - `HADOOP_HOME and hadoop.home.dir are unset` on Windows: this is a warning, not an error. You can ignore it.

---

## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Install Java and the Spark tutorial environment with uv
    - [x] Configure the environment variables Spark needs
    - [x] Run a Spark notebook from JupyterLab or VS Code
