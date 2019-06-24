# Cloud Scheduler to start and stop Compute Engine instances 

## Index

### Introductions

This tutorial demonstrates how to create, deploy and use cloud scheduler , cloud pub/sub and cloud functions on Google Cloud Platform using Python SDK. With Python SDKs, many of your dependent resources for this tutorial such as projects, IAM policies and service accounts can be easily recreated for your organization or teams.

### Objectives

- Create a service account and grant necessary permissions to the service account.
- Write and deploy cloud functions in python to start & stop compute instances.
- Write and deploy cloud scheduler to trigger cloud pub/sub at pre-defined time to start and stop compute instances.
- Write and deploy pub/sub topics to start and stop instances.

**Figure 1:** Architecture diagram 
![provision cloud pub/sub, cloud functions and cloud scheduler.
](./images/architecture_pubsub_fnc_scheduler.png)
Use gcloud and python SDK to provision cloud pub/sub, cloud functions and cloud scheduler.

### Pre-requisites


1. Setup gcloud 

Changes in this tutorial made without python SDK are done with the Google Cloud SDK gcloud command-line tool. This tutorial assumes that you have this tool installed and authorized to work with your account per the documentation.

2. create a service account with 3 roles 
     - Cloud Scheduler admin
     - service account token creator
     - service account user
  
  `Example:`
 ![ See image below :](./images/service_account_svc_cloud_scheduler.png)
                 

### How to deploy cloud functions

- Cloud Functions can be triggered by messages published to Cloud Pub/Sub topics in the `same GCP project as the function`. 
- Cloud Pub/Sub is a `globally distributed` message bus that automatically scales as you need it and provides a foundation for building your own robust, global services.

### Event Structure
- Cloud Functions triggered from Cloud Pub/Sub topic events will be sent an event containing a `PubsubMessage object`. 
- The `format` of the `PubsubMessage` is as per the published format for `PubsubMessage objects`.

- The payload of the `PubsubMessage` (the data you published to the topic) is stored as a `base64-encoded string` in the data attribute of the PubsubMessage. To extract the payload of the PubsubMessage you need to decode the data attribute.

Option1 : Using gcloud command

```python
gcloud functions deploy stop_instances --runtime python37 --trigger-resource T
OPIC_STOP_INSTANCES --trigger-event google.pubsub.topic.publish
```

- deploy : < Name of your cloud function >
- --runtime : <You can choose from `Node.js v6` ,`Nodejs v8` & `Python3.7`>
- --trigger-resource :< Name of your pub/sub Topic >
- --trigger-event : < How do you want to trigger it eg. by publishing to pubsub >

where TOPIC_NAME is the name of the Cloud Pub/Sub topic to which the function will be subscribed. If the topic doesn't exist, it is created during deployment.

### How to check cloud function logs 

```Python
gcloud functions logs read --limit 50
```

#### Output

```out
➜  gcp-cloudfunctions gcloud functions logs read --limit 50
LEVEL  NAME             EXECUTION_ID     TIME_UTC                 LOG
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'operationType': 'start',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'progress': 100,
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'selfLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/operations/operation-1542927421767-57b48c8e37d5a-73f89149-f22fb0c0',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'startTime': '2018-11-22T14:57:02.311-08:00',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'status': 'DONE',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'targetId': '1148048252264595239',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'targetLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/instances/instance-2',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'user': 'vantage2018-gke@appspot.gserviceaccount.com',
I      start_instances  304086077091116  2018-11-22 22:57:02.484   'zone': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a'}
D      start_instances  304086077091116  2018-11-22 22:57:02.488  Function execution took 1269 ms, finished with status: 'ok'
D      start_instances  304084106893746  2018-11-22 22:58:00.319  Function execution started
I      start_instances  304084106893746  2018-11-22 22:58:00.327  URL being requested: GET https://www.googleapis.com/discovery/v1/apis/compute/v1/rest
I      start_instances  304084106893746  2018-11-22 22:58:00.761  project_id : vantage2018-gke, zone_id: australia-southeast1-a, instance_name: instance-2, topic_name: Message number 24!
I      start_instances  304084106893746  2018-11-22 22:58:00.854  URL being requested: POST https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/instances/instance-2/start?alt=json
I      start_instances  304084106893746  2018-11-22 22:58:00.854  Attempting refresh to obtain initial access_token
I      start_instances  304084106893746  2018-11-22 22:58:01.770  {'endTime': '2018-11-22T14:58:01.505-08:00',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'id': '6679774801606380182',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'insertTime': '2018-11-22T14:58:01.501-08:00',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'kind': 'compute#operation',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'name': 'operation-1542927480961-57b48cc6ab7e9-23d5b677-b5426a58',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'operationType': 'start',
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'progress': 100,
I      start_instances  304084106893746  2018-11-22 22:58:01.770   'selfLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/operations/operation-1542927480961-57b48cc6ab7e9-23d5b677-b5426a58',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'startTime': '2018-11-22T14:58:01.505-08:00',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'status': 'DONE',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'targetId': '1148048252264595239',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'targetLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/instances/instance-2',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'user': 'vantage2018-gke@appspot.gserviceaccount.com',
I      start_instances  304084106893746  2018-11-22 22:58:01.771   'zone': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a'}
D      start_instances  304084106893746  2018-11-22 22:58:01.851  Function execution took 1533 ms, finished with status: 'ok'
D      start_instances  304089063332803  2018-11-22 22:59:00.474  Function execution started
I      start_instances  304089063332803  2018-11-22 22:59:00.480  URL being requested: GET https://www.googleapis.com/discovery/v1/apis/compute/v1/rest
I      start_instances  304089063332803  2018-11-22 22:59:00.957  project_id : vantage2018-gke, zone_id: australia-southeast1-a, instance_name: instance-2, topic_name: Message number 24!
I      start_instances  304089063332803  2018-11-22 22:59:01.052  URL being requested: POST https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/instances/instance-2/start?alt=json
I      start_instances  304089063332803  2018-11-22 22:59:01.052  Attempting refresh to obtain initial access_token
I      start_instances  304089063332803  2018-11-22 22:59:01.803  {'endTime': '2018-11-22T14:59:01.630-08:00',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'id': '2550852337134111322',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'insertTime': '2018-11-22T14:59:01.627-08:00',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'kind': 'compute#operation',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'name': 'operation-1542927541154-57b48d00130d1-40171f44-3ae48cd2',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'operationType': 'start',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'progress': 100,
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'selfLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/operations/operation-1542927541154-57b48d00130d1-40171f44-3ae48cd2',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'startTime': '2018-11-22T14:59:01.630-08:00',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'status': 'DONE',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'targetId': '1148048252264595239',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'targetLink': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a/instances/instance-2',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'user': 'vantage2018-gke@appspot.gserviceaccount.com',
I      start_instances  304089063332803  2018-11-22 22:59:01.803   'zone': 'https://www.googleapis.com/compute/v1/projects/vantage2018-gke/zones/australia-southeast1-a'}
D      start_instances  304089063332803  2018-11-22 22:59:01.807  Function execution took 1334 ms, finished with status: 'ok'
➜  gcp-cloudfunctions

```

## How to deploy cloud scheduler using python sdk

1. Change into the directory that holds your code
```
cd cloud_scheduler
``` 
2. Activate virtual env for python so that you have an isolated environment and all the necessary modules.

```
source setup/venv/venv_cloud_scheduler/bin/activate
```
3. use python to deploy
   
   Before you deploy ,update the inputs to the below variables 

- PROJECT_ID = "the ID of your project where you want to deploy this cloud scheduler"

- LOCATION_ID = " Provide the location where you want to deplpy"
Currently only 3 regions are supported US , europe and asia...

`example`:
LOCATION_ID = "us-central1"

- JOB_NAME
Update with the name of the job
`example`:
JOB_NAME = 'start_instances_at_9am'

The command to deploy is as below.

```python cloud_scheduler_start_instances.py``` 
