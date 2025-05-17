import os
import json
import requests

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
            'Content-Type': 'application/json'
        }
        start_response('200 OK', list(headers.items()))
        return [b'']

    elif environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body = environ['wsgi.input'].read().decode('utf-8')
            data = json.loads(request_body)
            user_message = data.get('input_value')
            # session_id = data.get('session_id')
            session_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

            langflow_api_key = os.environ.get('LANGFLOW_API_KEY')
            if not langflow_api_key:
                status = '500 Internal Server Error'
                headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
                start_response(status, list(headers.items()))
                return [json.dumps({'error': 'LANGFLOW_API_KEY environment variable not found.'}).encode('utf-8')]

            langflow_url = 'https://langflow.dev.aiprojectx.de/api/v1/run/31e780e0-3529-4e67-a60f-5f778a28e8b1'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': langflow_api_key
            }
            payload = json.dumps({
                'input_value': user_message,
                'output_type': 'chat',
                'input_type': 'chat',
                'session_id': session_id
            })

            print(f"Sending to Langflow: {payload}")  # Log the payload

            langflow_response = requests.post(langflow_url, headers=headers, data=payload)
            langflow_response.raise_for_status()  # Raise an exception for HTTP errors
            langflow_data = langflow_response.json()

            print(f"Received from Langflow: {json.dumps(langflow_data, indent=2)}")  # Log the entire response

            chat_output = None
            if (langflow_data and langflow_data.get('outputs') and len(langflow_data['outputs']) > 0 and
                    langflow_data['outputs'][0].get('outputs') and len(langflow_data['outputs'][0]['outputs']) > 0 and
                    langflow_data['outputs'][0]['outputs'][0].get('results') and
                    langflow_data['outputs'][0]['outputs'][0]['results'].get('message') and
                    langflow_data['outputs'][0]['outputs'][0]['results']['message'].get('data') and
                    langflow_data['outputs'][0]['outputs'][0]['results']['message']['data'].get('text')):
                chat_output = langflow_data['outputs'][0]['outputs'][0]['results']['message']['data']['text']

            status = '200 OK'
            headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            start_response(status, list(headers.items()))
            return [json.dumps({'output': chat_output}).encode('utf-8')] # Send the extracted output

        except requests.exceptions.RequestException as e:
            status = '500 Internal Server Error'
            headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            start_response(status, list(headers.items()))
            return [json.dumps({'error': f'Error communicating with Langflow API: {str(e)}'}).encode('utf-8')]
        except json.JSONDecodeError:
            status = '400 Bad Request'
            headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            start_response(status, list(headers.items()))
            return [json.dumps({'error': 'Invalid JSON in request body.'}).encode('utf-8')]
        except Exception as e:
            status = '500 Internal Server Error'
            headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            start_response(status, list(headers.items()))
            return [json.dumps({'error': f'An unexpected error occurred: {str(e)}'}).encode('utf-8')]
    else:
        status = '405 Method Not Allowed'
        headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        start_response(status, list(headers.items()))
        return [json.dumps({'error': 'Method Not Allowed'}).encode('utf-8')]