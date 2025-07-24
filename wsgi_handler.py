import json
import base64
from io import StringIO
import sys
from urllib.parse import unquote_plus

from app import app

def handler(event, context):
    """
    AWS Lambda handler that converts API Gateway events to Flask requests
    """
    
    # Handle different event formats (API Gateway v1 vs v2)
    if 'requestContext' in event and 'http' in event['requestContext']:
        # API Gateway v2 format
        path = event['rawPath'] if 'rawPath' in event else '/'
        method = event['requestContext']['http']['method']
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters') or {}
        body = event.get('body', '')
    else:
        # API Gateway v1 format or other
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters') or {}
        body = event.get('body', '')
    
    # Handle base64 encoded body
    if event.get('isBase64Encoded', False) and body:
        body = base64.b64decode(body).decode('utf-8')
    
    # Create WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': unquote_plus(path),
        'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items()]) if query_params else '',
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)) if body else '0',
        'SERVER_NAME': headers.get('host', 'localhost').split(':')[0],
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': StringIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Capture response
    response_data = {}
    
    def start_response(status, response_headers, exc_info=None):
        response_data['status'] = int(status.split(' ')[0])
        response_data['headers'] = dict(response_headers)
        return lambda x: None
    
    # Call Flask app
    with app.app_context():
        response = app.wsgi_app(environ, start_response)
        response_body = b''.join(response).decode('utf-8')
    
    # Return API Gateway response format
    return {
        'statusCode': response_data.get('status', 200),
        'headers': response_data.get('headers', {}),
        'body': response_body,
        'isBase64Encoded': False
    }