'''
Encapsulates all tasks that can be run against the 'webhooks' endpoint
'''
def _check_url_length(url, api):
    ''' Checks the given url against the given API specifications to ensure it's short enough '''
    if len(url) > api.MAX_WEBHOOK_URL_LENGTH:
        raise ValueError("Url cannot be longer than {} characters".format(api.MAX_WEBHOOK_URL_LENGTH))

def get_webhooks(client, list_id):
    ''' Gets all webhooks for the given list ID '''
    params = { 
            'list_id' : str(list_id)
            }
    response = client.authenticated_request(client.api.Endpoints.WEBHOOKS, params=params)
    return response.json()

def create_webhook(client, list_id, url, processor_type, configuration=""):
    ''' 
    Creates a webhook in the given list

    See https://developer.wunderlist.com/documentation/endpoints/webhooks for detailed parameter information
    '''
    _check_url_length(url, client.api)
    data = {
            'list_id' : int(list_id) if list_id else None,
            'url' : url,
            'processor_type' : processor_type,
            'configuration' : configuration
            }
    data = { key: value for key, value in data.iteritems() if value is not None }
    response = client.authenticated_request(client.api.Endpoints.WEBHOOKS, 'POST', data=data)
    return response.json()

def delete_webhook(client, webhook_id, revision):
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.WEBHOOKS, str(webhook_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)
