from google.cloud import scheduler_v1beta1
import base64
import httplib2
from pprint import pprint
from google.oauth2 import service_account
# import googleapiclient.discovery
SCOPES = ['https://www.googleapis.com/auth/cloud-scheduler',
          'https://www.googleapis.com/auth/cloud-platform']

SERVICE_ACCOUNT_FILE = '../auth/firewall-management-dd391be3d8df.json'

PROJECT_ID = "firewall-management"
LOCATION_ID = "asia-northeast1"
JOB_ZONE_ID = "australia-southeast1-c"
INSTANCE_ID = "oreta-fw-mgmt-server"
JOB_NAME = 'stop_instances_at_430pm'
JOB_DESCRIPTION = 'This Job will execute everyday at 4:30pm and stop an instance'
SCHEDULE_DEFINITION = "30 16 *  * *"
TOPIC_NAME = "projects/firewall-management/topics/TOPIC_STOP_INSTANCES"

# Construct credentials to use service accounts and required scopes
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
print(credentials)


# API REFERENCE :https://googleapis.github.io/google-cloud-python/latest/scheduler/gapic/v1beta1/api.html
# Contruct the client to make Cloud Scheduler calls


client = scheduler_v1beta1.CloudSchedulerClient(credentials=credentials)

# Contruct the parent to create the location path
parent = client.location_path(PROJECT_ID, LOCATION_ID)
print(parent)
# Contruct the job path using the job_path method 
name = client.job_path(PROJECT_ID, LOCATION_ID, JOB_NAME)
print("name: {}".format(name))

## the variable n is used to set the Message number ,its random and just for testing purpose ,
# TODO change the logic for data variable.
n = 24
data = u'Message number {}'.format(n)
# Data must be a bytestring
data = data.encode('utf-8')

## Below is the Job definition and the payload for pubsub that matches with inputs for defined cloudfunctions.
job = {
    "name": name,
    "description": JOB_DESCRIPTION,
    "schedule": SCHEDULE_DEFINITION,
    "time_zone": "Australia/Sydney",
    "pubsub_target": {
            "topic_name": TOPIC_NAME,
            "data": data,
            "attributes": {
                "project_id": PROJECT_ID,
                "zone_id": "australia-southeast1-c",
                "instance_id": INSTANCE_ID
            }
        }
    }

response1 = client.create_job(parent, job)
print(response1)
