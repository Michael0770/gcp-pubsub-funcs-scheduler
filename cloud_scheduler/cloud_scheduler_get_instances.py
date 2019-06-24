from google.cloud import scheduler_v1beta1
import base64
import httplib2
from pprint import pprint
from google.oauth2 import service_account
import googleapiclient.discovery
SCOPES = ['https://www.googleapis.com/auth/cloud-scheduler',
          'https://www.googleapis.com/auth/cloud-platform']

SERVICE_ACCOUNT_FILE = '../../auth/vantage2018-gke-809963f91f38.json'

PROJECT_ID = "vantage2018-gke"
LOCATION_ID = "us-central1"
JOB_NAME = 'test_start_auto_py'
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

# https://stackoverflow.com/questions/46102807/getting-403-error-when-accessing-google-my-business-api-through-service-account


response = client.get_job(name)
print(response)
