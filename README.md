Apache-Airflow
============================   

Airflow is a platform to:    
* Programmatically author
* Schedule
* Monitor workflows


## Installation

### 1. Running Airflow in Ubuntu/WSL -   
Note: For using WSL, ensure WSL is installed. Or, to install WSL use the following link - [https://docs.microsoft.com/en-us/windows/wsl/install-manual](https://docs.microsoft.com/en-us/windows/wsl/install-manual)  
STEP 1: Update the system
```bash
$ sudo apt-get update
```

STEP 2: Install the required packages.

```bash
$ apt-get install software-properties-common
$ apt-add-repository universe
```

STEP 3: Update the packages.

```bash
$ apt-get update
```


STEP 4: Install the python3-pip.

```bash
$ apt-get install python-setuptools
$ apt install python3-pip
```

STEP 5: Install the required dependencies for Apache Airflow.

```bash
$ apt-get install libmysqlclient-dev
$ apt-get install libssl-dev
$ apt-get install libkrb5-dev
```

STEP 6: Installing Apache-Airflow on the system.   

I. Install the python-virtual Environment.
```bash
$ apt install python3-virtualenv
$ virtualenv -p python venv
```
II.  Activate the source.
```bash
$ source venv/bin/activate
```
III.  Now ,install the apache-airflow.
```bash
$ export AIRFLOW_HOME=~/airflow
$ pip3 install apache-airflow
```
IV. Install typing_extension.
```bash
$ pip3 install typing_extensions
```
V. Run the following command (This command  is to be used only the first time that the database is created from the airflow.cfg).
```bash
$ airflow db init
```
VI. Set the Apache-Airflow login credentials for airflow web interface.
```bash
$ airflow users create --username admin --firstname FIRST_NAME --lastname  LAST_NAME --role Admin --email admin@example.org --password admin
```
For example - 
```bash
$ airflow users create --username admin --firstname admin --lastname testing --role Admin --email admin@domain.com --password admin
```
Note: There are five default roles: Public, Viewer, User, Op, and Admin. Each one has the permissions of the preceding role, as well as additional permissions.

VII. Start the Apache-Airflow web interface
```bash
$ airflow webserver
```
Go to: [http://localhost:8080/](http://localhost:8080/) to view the Airflow UI. 

VIII. Start the airflow scheduler (in a separate terminal)
```bash	
$ airflow scheduler
```

### 2. Running Aiflow using Docker
STEP 1: Fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml)

The first thing we’ll need is the docker-compose.yaml file. Create a new directory on your home directory (let’s call it airflow-local):
```bash
$ mkdir airflow-local
$ cd airflow-local
```
And fetch the docker-compose.yaml file (note that we will be using Airflow v2.3.0)

```bash
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'
```
Note: the services defined in it namely airflow-scheduler, airflow-webserver, airflow-worker, airflow-init, flower, postgres and redis.


Step 2: Create directories
Now while you are in the airflow-local directory, we will need to create three additional directories:
* dags
* logs
* Plugins
```bash
$ mkdir ./dags ./logs ./plugins
```
Step 3: Setting the Airflow user

Now we would have to export an environment variable to ensure that the folder on your host machine and the folders within the containers share the same permissions. We will simply add these variables into a file called .env.
```bash
$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

Inspect the content of .env using cat and ensure that it contains the two aforementioned variables.
```bash
$ cat .env
```

Step 4: Initialise the Airflow Database

Now we are ready initialise the Airflow Database by first starting the airflow-init container:

```bash
$ docker-compose up airflow-init
```

This service will essentially run airflow db init and create the admin user for the Airflow Database. By default, the account created has the login *airflow* and the password *airflow*.

Step 5: Start Airflow services
The final thing we need to do to get Airflow up and running is start the Airflow services we’ve seen in Step 1.

```bash
$ docker-compose up
```

Note that the above command may take a while since multiple services need to be started. Once done, you can verify that these images are up and running using the following command in a new command-line tab:

```bash
$ docker ps
```

Step 6: Access Airflow UI
In order to access Airflow User Interface simply head to your preferred browser and open [localhost:8080](localhost:8080).


Step 7: Cleaning up the mess
Once you are done with your experimentation, you can clean up the mess we’ve just created by simply running

```bash
$ docker-compose down --volumes --rmi all
```

This command will stop and delete all running containers, delete volumes with database data and downloaded images.
If you run docker ps once again you can verify that no container is up and running

```bash
$ docker ps
```
