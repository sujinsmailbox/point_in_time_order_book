# Setting up the Environment

This repository runs a MYSQL instance in docker which is used for storing and retrieving the data

## Prerequisites

- **macOS**: [Install Docker Desktop](https://docs.docker.com/desktop/).
- **Linux/Ubuntu**: [Install Docker Compose](https://docs.docker.com/compose/install/) and [Install Docker Engine](https://docs.docker.com/engine/install/).
- **Windows**: Windows Subsystem for Linux (WSL) to run the bash based command `mwaa-local-env`. Please follow [Windows Subsystem for Linux Installation (WSL)](https://docs.docker.com/docker-for-windows/wsl/) and [Using Docker in WSL 2](https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2), to get started.

* For windows Setup, you may need to change the line endings of bash files
* Windows might have problem in operating volumes hosted in windows from docker instances


## Get started

```bash
git clone https://github.com/sujinsmailbox/point_in_time_order_book
cd point_in_time_order_book

```

### Step one: Building the Docker image

Build the Docker container image using the following command:

```bash
./build-local-env
```

**Note**: it takes several minutes to build the Docker image locally.

### Step two: Running the application

#### Prerequisites: Python installed in your machine

run the main file of the project from your local

```
python3 main.py
```

The code will first run the database queries for setting up the data 
and the inserts the data into the table and once that is ready, It will prompt to enter the `timestamp` and `symbol` name

First time the system will query the database and returns the value. Paralelly it will update the value in cache aswell. 
From next time, the values will be retrieved from cache, If the values are available in cache, if not, it will go for a database query

In a wider implementation, considering the scalability, performance and latency for data retrieval. It's best to have the results stored in a database and Elastic Cache, 
Recent results are maintained in  Redis

We can use micro services architecture for data retrieval which is coupled with cache maintainenance, DB insertion/retrieval. 



