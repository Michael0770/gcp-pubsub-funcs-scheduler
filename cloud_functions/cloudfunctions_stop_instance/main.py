def stop_instances(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    import base64
    from pprint import pprint
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials, cache_discovery=False)

    if 'attributes' in data:
        # name = base64.b64decode(data['data']).decode('utf-8')
        project = data['attributes']['project_id']
        zone = data['attributes']['zone_id']
        instance = data['attributes']['instance_id']
    else:
        # name = 'World'
        project = 'Not Provided'
        zone = 'Not Provided'
        instance = 'Not Provided'

    if 'data' in data:
        name = base64.b64decode(data['data']).decode('utf-8')
    else:
        name = 'World'
    # print('Hello, {0},!'.format(name))
    print('project_id : {0}, zone_id: {1}, instance_name: {2}, topic_name: {3}!'.format(project, zone, instance, name))

    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
    # TODO: Change code below to process the `response` dict:
    pprint(response)

    