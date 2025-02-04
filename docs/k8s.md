# Advanced Deployment with Kubernetes

In this tutorial, we will cover as much Kubernetes practices as we can.

You can play with a sandboxed Kubernetes (often abbreviated k8s) on:

* [Play with Kubernetes](https://labs.play-with-k8s.com/) following [this classroom](https://training.play-with-kubernetes.com/kubernetes-workshop/)

...but I'd rather you provision your own local K8s cluster.

## Prerequisites

* Docker Desktop

## 1. Kubernetes Quick Start

![](./images/kubernetes-logo.png)

### a. Start Kubernetes

Docker Desktop comes with a deactivated K8s cluster which you can [start on demand](https://docs.docker.com/desktop/features/kubernetes/#install-and-turn-on-kubernetes).

!!! note "Exercise - Start Docker Desktop's K8s cluster"
    - Start up Docker Desktop, go to Settings, check `Enable Kubernetes` and apply & restart
        - When Kubernetes is enabled, its status is displayed in the Docker Desktop Dashboard footer and the Docker menu.
        - Like the `docker` command connects to the Docker cluster, `kubectl` is the command-line tool to run commands against a K8s cluster. 
    - Open a new Command Line terminal to run `kubectl version`
    - Display the cluster info with `kubectl cluster-info`
    - Display nodes in your cluster with `kubectl get nodes`

While Docker handles the creation and running of individual containers on a single host, Kubernetes extends this by orchestrating multiple containers across multiple hosts. 

It also includes scaling, load balancing, and self-healing of containerized applications.

In the next section, we will deploy multiple Docker images on this K8s cluster.

### b. Build Docker images of a FastAPI API

Let's build 3 versions of a Docker image to see how we can deploy and manage their lifecycle on a K8s cluster.

!!! note "Exercise - Build 1 Docker image in 3 different versions"
    - Create a new `app.py` with the following content:
    
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/version")
    async def version():
        return {"version": "0.1.0"}
    ```

    - Build a Docker image to expose this Python API. Tag it `api:0.1.0`
        - If you run `docker run --rm -p 8000:8000 api:0.1.0`, you should be able to ping the api on `http://localhost:8000`.
    - Edit the code to add a new endpoint and edit the version endpoint. 
    - Build this edited script into a new Docker image `api:0.2.0`
    - Repeat the process into a new Docker image `api:0.3.0`
  
### c. Deploy a Pod

The Pod is the smallest deployable unit in Kubernetes. Think of it as a small wrapper around a running container to make it run on Kubernetes.

The most common way to deploy on Kuberntes is by declarating what you want deployed in a YAML file. The YAML specification describes how we want our app to run on Kubernetes, and Kubernetes will do its best to move the current state of the app to match the spec.

!!! note "Exercise - Deploy the Dockerized API into a pod"
    - In a new folder `k8s`, 
    - Create a new `pod.yaml` file.
    - Edit its contents as: 
    
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: api-pod
      labels:
        app: api
        version: 0.1.0
    spec:
      containers:
      - name: api
        image: api:0.1.0
        ports:
        - containerPort: 8000
    ```

    - Declare the state you want to Kubernetes by applying the file, with the command `kubectl apply -f pod.yaml`.
    - Check all running pods on Kubernetes with `kubectl get pods`.
    - Get pod details: `kubectl get pod api-pod -o yaml`
    - Like in Docker, open a shell inside the pod: `kubectl exec -it api-pod -- /bin/bash`
    - Select pods with a specific label, example `kubectl get pods -l app=api`
    - Destroy the pod with: `kubectl delete pod api-pod`
        - Does the pod self-heal/reappear?

    ??? abstract "Here's a breakdown of the YAML file"
        ```yaml
        # The version of the Kubernetes API you're using
        apiVersion: v1

        # What type of resource you're creating (Pod, Deployment, Service, etc.)
        kind: Pod

        # Metadata about the resource (name, labels, etc.)
        metadata:
        name: api-pod          # The name of your pod
        labels:                # Labels are key-value pairs used for organizing and selecting resources
            app: api            # Example label: app=api

        # The actual specification of what you want to create
        spec:
        containers:           # List of containers in the pod
        - name: api           # Name of the container
            image: api:0.1.0    # Docker image to use
            ports:              # Ports to expose
            - containerPort: 8080  # Port the container listens on
        ```

Now that you have run your Docker image in a Pod on Kubernetes, let's start more pods.

!!! note "Exercise - Deploy more pooodddsss"
    - Edit `pod.yaml` to start 3 pods, 1 per version

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
    name: api-pod-1
    labels:
        app: api
        version: 0.1.0
    spec:
    containers:
    - name: api
        image: api:0.1.0
        ports:
        - containerPort: 8000
    ---
    apiVersion: v1
    kind: Pod
    metadata:
    name: api-pod-2
    labels:
        app: api
        version: 0.2.0
    spec:
    containers:
    - name: api
        image: api:0.2.0
        ports:
        - containerPort: 8000
    ---
    apiVersion: v1
    kind: Pod
    metadata:
    name: api-pod-3
    labels:
        app: api
        version: 0.3.0
    spec:
    containers:
    - name: api
        image: api:0.3.0
        ports:
        - containerPort: 8000
    ```

    - Re-apply the declarative spec: `kubectl apply -f pod.yaml`
    - List all pods: `kubectl get pods`
    - Delete the second one: `kubectl delete pod api-pod-2`. Does it self-heal?
    - Rerun `kubectl apply -f pod.yaml`. What do you think happened to each pod?
    - Delete all pods by declaring the deletion of the yaml file: `kubectl delete -f pod.yaml`.