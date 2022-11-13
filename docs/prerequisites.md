# TD0 - Prerequisites

For this tutorial, you will be installing and configuring the tools used in the following tutorials

![](./images/cover-prerequisites.jpg)

## Objectives

- [ ] Get the Hadoop ecosystem running inside a virtual machine
- [ ] Build a new conda environment with some of the necessary packages installed

---

## The Hortonworks Virtual Machine

Before working on the Hadoop tutorial, we need a working Hadoop cluster. It won't be easy for us to get one on the Cloud without giving up an email or credit card details, so we are going to install one locally, using:

- [VirtualBox](https://www.virtualbox.org/) to run the virtual machine.
- [Hortonworks Sandbox 2.5.0](https://www.cloudera.com/downloads/hortonworks-sandbox.html). It is less demanding in terms of resources than version 3+ and sufficient for our needs.

!!! warning
    While it is technically possible to download and use a VMWare or Docker version of the virtual machine, it will be easier for your comrades and myself to help you if everybody uses the same Virtualbox version

### Exercise 

1. Ensure you have VirtualBox installed on your workstation
    - It should be, but if not, download and install VirtualBox [from this link](https://www.virtualbox.org/)
2. Download [Hortonworks Sandbox 2.5.0](https://www.cloudera.com/downloads/hortonworks-sandbox/hdp.html) and unzip the appliance for VirtualBox
    - You don't have to enter your info in the form
3. Import the `.ova` file into VirtualBox. **Don't start it yet** if you want to configure it
    - You may configure the VM to use more or less RAM depending on your machine, through the `Configuration > System` view. The recommended value is around 6-8 Go RAM, but you should get away with using 2-4 Go
4. Start the virtual machine with the `Start` green arrow. This may take a few minutes
    - If the virtual machine stops during startup, it is generally because you don't have enough resources. Try to open a process manager and kill some RAM-consuming processes, or lower the RAM needed by the virtual machine using the above step
5. Open a web browser to [http://localhost:8888](http://localhost:8888) to be greeted with the Hortonworks Data Platform dashboard

![](./images/hdp-dashboard.png)

!!! tip 
    When you're done, you're free to stop the virtual machine from the Virtualbox dashboard.

!!! question
    With 1 or 2 neighbors, brainstorm and **write down** use cases for using a virtual machine in a company. Yes I may be passing in the ranks to see your solutions.

---

## Anaconda to configure our Python environment 

While you usually install and use [Anaconda](https://docs.anaconda.com/) as a Python distribution with a lot of Data Science packages preinstalled, Anaconda comes with a package and environment manager called `conda`. You may have seen the list of environments managed by your current conda installation when browsing the Anaconda Navigator.

![](./images/anaconda-navigator.PNG)

In the following, we won't be using the Anaconda Navigator UI. Brush up your bash skills, command-line is life :smiling_imp:. The [Conda Cheatsheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) will definitely be of help.

### Exercise 

1. Open the Anaconda prompt from the Start Menu.
2. Create a new environment (with any name you'd like) with python 3.8 installed.
3. Ensure your environment is present by listing all current conda environments.
4. You need to `activate` your conda environment to access its `python`, `pip` and `conda` environment-specific commands. What command is responsible for this? When used, how do you know you're in the correct environment?
    - To ensure Python is properly installed, run `python -m http.server` to have Python run an HTTP server on `http:::localhost:8000`.
5. We now install some packages in your newly created and activated environment:
    - Use the `conda install` command to install git. Test the git command by cloning any project from [Github](https://github.com/) to your workstation.
    - Use the `pip install` command to install Jupyter Notebook and JupyterLab. Test the `jupyter lab` command to ensure it works


!!! tip
    Get in the habit of installing every Python package with pip and every non-Python one with conda

!!! question
    Explain to a comrade your view on the difference between conda and pip. Then invert the roles and listen to his/her explanation. Compare the explanations. Notice where you agree and disagree, feel free to ask more people until you are happy with your understanding of the question.


## Recap

!!! success "Check that you can teach your neighbor each point of the checklist below"
    - [x] Get the Hadoop ecosystem running inside a virtual machine
    - [x] Build a new conda environment with some of the necessary packages installed

In the next tutorial, we will build our own ETL-like solution in Hadoop. We will have a look at ingesting unstructured data live to HDFS, extracting and structuring the important information into a Hive table, and build simple graphs.