from google.cloud import scheduler_v1beta1
import base64
import httplib2
from pprint import pprint
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/cloud-scheduler',
          'https://www.googleapis.com/auth/cloud-platform']

# We can drop the scope cloud-platform it was used during testing 
SERVICE_ACCOUNT_FILE = '../auth/firewall-management-dd391be3d8df.json'

PROJECT_ID = "firewall-management"
LOCATION_ID = "asia-northeast1"
JOB_NAME = 'start_instances_at_345pm'
JOB_NAME1 = 'test1'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
print(credentials)


# API REFERENCE :https://googleapis.github.io/google-cloud-python/latest/scheduler/gapic/v1beta1/api.html
# Contruct the client to make Cloud Scheduler calls


client = scheduler_v1beta1.CloudSchedulerClient(credentials=credentials)
parent = client.location_path(PROJECT_ID, LOCATION_ID)
print(parent)
name = client.job_path(PROJECT_ID, LOCATION_ID, JOB_NAME)
print("name: {}".format(name))
# name1 = client.job_path(PROJECT_ID, LOCATION_ID, JOB_NAME1)
# print("name1: {}".format(name1))

n = 24
data = u'Message number {}'.format(n)
# Data must be a bytestring
data = data.encode('utf-8')


job = {
    "name": name,
    "description": "start_instances_at_3:45pm",
    "schedule": "45 15 *  * *",
    "time_zone": "Australia/Sydney",
    "pubsub_target": {
            "topic_name": "projects/firewall-management/topics/TOPIC_START_INSTANCES",
            "data": data,
            "attributes": {
                "project_id": "firewall-management",
                "zone_id": "australia-southeast1-c",
                "instance_id": "oreta-fw-mgmt-server"
            }
        }
    }

response1 = client.create_job(parent, job)
print(response1)
