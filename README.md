<p align=center><img src=_src/assets/mox.jpg><p>

# <h1 align=center> **Credit Scoring System with Machine Learning** </h1>

# Introduction

This is a project for a Mexican Fintech that want to implement a credit scoring system using machine learning techniques. 

# About MOX

MOX is a startup focused on OpenData in order to automate and streamline the pre-qualification, 
origination and collection processes for financial entities in Mexico. One of MOX's solutions 
consists of a platform that allows viewing data on income/employment/pensions of credit applicants 
in real time.


# Project Overview

The main objective of the project is to provide clients with a useful tool to qualify profiles and 
evaluate the repayment ability of applicants for all types of personal loans and credits. The income 
score will be built using individual information from the profile, as well as external data 
(demographic data, national surveys/household surveys, among other datasets) that refer to your 
environment. This combination of information will allow obtaining a clearer and more precise image 
of the financial situation of each person. To give customers a better understanding of each 
profile's ability to pay, alternate credit scores are used. Customers will be able to issue credit 
in an informed and data-driven manner by using the score as a quantitative indicator.<br>
<br>
The main advantage of the income score built in this project lies in the combination of individual 
profile information and external data referring to its environment. By considering factors such as 
income, job seniority, number of jobs in recent years, age, state/province, income growth, 
education, type and behavior of the industry, and social status of the population, a more complete 
and comprehensive perspective is obtained. accurate profile of the applicant. Some of these 
variables are obtained directly from the MOX datasets such as the specific variables of the profile, 
the other variables about their environment will be obtained from public databases, open government 
data and surveys.<br>
<br>
The deliverable of the project is to create a score that gathers the different data around the 
requested profile and immediately offers a balanced metric for easy classification of the profile.

## Repository content

- .dvc/: DVC configuration files.
- .github/workflows/: Github Actions.
- .streamlit/: Frontend configurations.
- api/: API development.
- business_rules/: JSON file with business rules.
- dataset/: Dataset files.
- frontend/: Frontend development.
- model/: machine learning models files.
- notebooks/: Notebooks file with etl and machine learning.
- src/: Training scripts files.
- testing/: API test files.
- utilities/: Utils functions.
- …: Miscellaneous project files.

## The main tasks that are executed in the pipeline

- Cloning the working main branch.
- Creation of a virtual environment.
- Installation of dependencies (requirements.txt).
- Configuration of environment variables to be able to access the GCP storage.
- Acquisition of the models and datasets stored in the GCP storage using the DVC tool.
- Execution of the ETL script and the Machine Learning script which will generate new models and new datasets.
- Storage of the new models and datasets created in the GCP storage using the DVC tool.
- Update of the git repository with the new files that contain the reference to the previously created models and datasets.
- Publication of the most important metrics and sending information to the email address configured to monitor the status of the model.


<p align=center><img src=_src/assets/tasks.png><p>



## GCP Storage Configuration

- Create a new project.

<p align=center><img src=_src/assets/new_project.png><p>

- Go to APIs and Services -> Credentials.

<p align=center><img src=_src/assets/api_service.png><p>

- Create a new Service Account credentials.

<p align=center><img src=_src/assets/create_credential.png><p>

- Set a name that will be used by DVC forward.
- Permission asigment:  Storage -> Cloud Storage -> Storage Admin
- Go to the storage created and download the JSON credential.

<p align=center><img src=_src/assets/storage.png><p>
<p align=center><img src=_src/assets/storage_key.png><p>
<p align=center><img src=_src/assets/storage_key_json.png><p>

- Store the key in the project.

### Create a Bucket to store the serialized data (datasets and models).

- Go to Cloud Storage -> Bucket -> Create

<p align=center><img src=_src/assets/create_bucket.png><p>
<p align=center><img src=_src/assets/create_bucket_1.png><p>

- Set a name.
- Other field by default.
- Create a folder for dataset and for models


## DVC (Data Version Control) Initialization

- Install dvc and dvc-gs dependencies

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
dvc init
```
- Once the JSON credential of the previous steps is downloaded and copied into the porject, set the environment variable as follow:

```
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath <credential-file>.json)
```

- Check the environment variable:

```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

- Connect DVC with the GCP remote bucket

```
dvc remote add <bucket-reference> gs://<bucket-name>/<folder>
```
bucket-reference: Name to refer to the storage, this name will be stored in `.dvc/config` file.
bucket-name: Use the same bucket name sets in the `GCP Storage Configuration` step. 
folder: Folder created in the bucket to storage elements.


Example:

For the dataset folder we can use:

```
dvc remote add dataset-track gs://model-and-dataset-tracker/dataset
```

For the model folder we can use:

```
dvc remote add model-track gs://model-and-dataset-tracker/model
```

In order to create a local or manual deployment we can storage the CSV (datasets) and PKL (models) manually (in case files do not exist read the next section). To do so

```
dvc add <file-name>
dvc push <file-name> -r <bucket-reference>
```
Where <bucket-reference> is stored in `.dvc/config` file.

Example:

```
dvc add model/model.pkl
dvc push model/model.pkl -r model-track
```

### CVS and Model creation

In case the `PKL` files in the `model` folder and `data_prueba_limpia.csv` file in the `dataset` folder do not exist, run the following command to create them:

```
dvc repro -f
```

This command will excecute the `dvc.yaml` and it will run the `notebooks/etl_process.ipynb` to create the `data_prueba_limpia.csv` file. After the excecution it will run the `notebooks/models.ipynb` to create the machine learning models.

Once those file are created can be storage and tracked with DVC following the steps in the ***DVC (Data Version Control) Initialization** section.


## Create GCP credentials to deploy with Github Actions

- Go to APIs and Services in the left tab -> Credentials

<p align=center><img src=_src/assets/service.png><p>

- Create credentials -> Service Account

<p align=center><img src=_src/assets/credentials.png><p>

- Set a name and continue.
- Set the following roles:
  - Cloud Storage -> Storage admin (Cloud storage control)
  - Cloud Run -> Cloud Run admin (Cloud run resource control)
  - Artifact Registry -> Artifact registry admin (create and admin repositories)
  - Service Account -> Service Account user (To deploy in cloud run)
- Select Ready

<p align=center><img src=_src/assets/ready.png><p>

- Once the account is created go to the account and add a JSON key.

<p align=center><img src=_src/assets/key.png><p>

- Copu the JSON file inside the project an in a shell console run the following command:

```
base64 <file-name>.json
```
- Copy the output
- Go to Github -> Setting -> Secrets and Variables -> Actions -> New Repository Secret

<p align=center><img src=_src/assets/secret.png><p>

- Create SERVICE_ACCOUNT_KEY secrete name and paste the `base64 <file-name>.json` output.


## Create a Cloud Run Service for the API

- Go to Cloud Run 

<p align=center><img src=_src/assets/cloud_run.png><p>

- Create Service

<p align=center><img src=_src/assets/create_service_cloud_run.png><p>

- Click in Select -> Container Registry -> Demo Container -> Hello -> Ok

<p align=center><img src=_src/assets/select.png><p>

- Set Service Name
- Set Region ``us-central1 (Iowa)
- Authentication -> Allow unauthenticated invocations
- Set Minimun Instance Number = 1
- Set Maximun Instance Number = 10 or greater
- Select Containers, Net tools, Security

<p align=center><img src=_src/assets/containers.png><p>

- Container Port = 8000
- Memory = 1Gb or greater
- Maximum number of concurrent requests per instance = 10 or greater
- Create

## Create a Cloud Run Service for the Frontend App

- Repeat the previous steps but set the Container Port to 8080

## Configure Github with secrets for Cloud Services

- Open Github and Add new secrets
- Go to Settings -> Secretes and Variables -> New Repository Secret

<p align=center><img src=_src/assets/secret.png><p>

The following secrets can be found in the Cloud Run Services created in the previous steps.

- Add REGION

<p align=center><img src=_src/assets/region.png><p>

>Note: The region can be found as the following picture shows

<p align=center><img src=_src/assets/region_gcp.png><p>

>Note: As both services created have the same region, one REGION secret is enough.

- Add REGISTRY_NAME 
- Add REGISTRY_NAME_FRONT
- Add PROJECT_ID

The REGISTRY_NAME and REGISTRY_NAME_FRONT can be created as follow:

gcr.io/<PROJECT_ID>/<NAME_REG>

Where NAME_REG is a name that we pick and PROJECT_ID can be found as follow.

<p align=center><img src=_src/assets/project_id.png><p>

Example

```
REGISTRY_NAME = gcr.io/mox-storage-project-test/scoring-ml
REGISTRY_NAME_FRONT = gcr.io/mox-storage-project-test/scoring-ml-frontend
PROJECT_ID = mox-storage-project-test
```

- Add SERVICE_NAME
- Add SERVICE_NAME_FRONT

>Note: The service_name and service_name front can be found as the following picture shows

<p align=center><img src=_src/assets/service_name.png><p>


At the end of these steps, the following secrets must be created in order to get the app working

<p align=center><img src=_src/assets/all_secrets.png><p>


## Local Deployment

For these steps the the environment variable must be set as follow:

```
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath <credential-file>.json)
```

Where `<credential-file>.json` was downloaded in the **GCP Storage Configuration** section

Check the environment variable:

```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

Run the docker compose file to deploy the project:

```
docker compose up -d --build
```

The frontend deployment can be found in the following browser path:

```
localhost:8080
```

The API deployment can be found in the following browser path:

```
localhost:8000
```

## Cloud Deployment

The cloud deployment was set to be automaticaly by Github Actions in the `.github/workflows/ci_cd.yaml` file, and it will be done everytime a `git push` command is excecuted into the `main` branch.


## Continuous Training

The continuous training was set to be automaticaly by Github Actions in the `.github/workflows/continuous_training.yaml` file, and it will be done everytime the cloud deployment is triggered or/and every day at midnight, set by a cron job.
To configure email report please configure the `.github/workflows/continuous_training.yaml` file with your own email as is shown in the picture below:

<p align=center><img src=_src/assets/email_git.png><p>
