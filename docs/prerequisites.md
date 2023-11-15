# TD0 - Tooling

For this tutorial, you will be installing and configuring tools used in the following tutorials:

- Command line
- Docker
- Git
- Conda
- Python librairies: Streamlit & FastAPI


![](./images/cover-prerequisites.jpg)

## Objectives

- [ ] Get used to using your command prompt
- [ ] Reinstall Docker to ensure a clean docker-compose environment
- [ ] Git clone the NoSQL or Spark tutorial
- [ ] Create a conda environment with Python 3.9, FastAPI and Streamlit

---

## Test your command line skills

---

## Repair your Docker environment

---

## Git clone a project

---

## Create a complete Python environment

While you usually install and use [Anaconda](https://docs.anaconda.com/) as a Python distribution with a lot of Data Science packages preinstalled, Anaconda comes with a package and environment manager called `conda`. You may have seen the list of environments managed by your current conda installation when browsing the Anaconda Navigator.

![](./images/anaconda-navigator.PNG)

In the following, we won't be using the Anaconda Navigator UI. Brush up your bash skills, command-line is life :smiling_imp:. The [Conda Cheatsheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) will definitely be of help.

!!! note "Exercise - Installing Conda environment"
    1. Open the Anaconda prompt from the Start Menu.
    2. Create a new environment (with any name you'd like) with python 3.8 installed.
    3. Ensure your environment is present by listing all current conda environments.
    4. You need to `activate` your conda environment to access its `python`, `pip` and `conda` environment-specific commands. What command is responsible for this? When used, how do you know you're in the correct environment?
        - To ensure Python is properly installed, run `python -m http.server` to have Python run an HTTP server on `http:::localhost:8000`.
    5. We now install some packages in your newly created and activated environment:
        - Use the `conda install` command to install git. Test the git command by cloning any project from [Github](https://github.com/) to your workstation.
        - Use the `pip install` command to install Jupyter Notebook and JupyterLab. Test the `jupyter lab` command to ensure it works    

!!! question
    - Explain to a comrade your view on the difference between conda and pip. Then invert the roles and listen to his/her explanation. Compare the explanations. Notice where you agree and disagree, feel free to ask more people until you are happy with your understanding of the question.
    - Why should you et in the habit of installing every Python package with pip and every non-Python one with conda?


## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Get used to using your command prompt
    - [x] Reinstall Docker to ensure a clean docker-compose environment
    - [x] Git clone the Spark tutorial
    - [x] Create a conda environment with Python 3.9, FastAPI and Streamlit 

In the next tutorial,