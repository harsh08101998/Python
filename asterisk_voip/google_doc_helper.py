from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# The ID of a sample document.
# DOCUMENT_ID = '1CHakZsudm1_WeOLavtyzMPzrKIDOqy69jIbcnr_TNN0'

def authenticate(service):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    if service == 'DOC':
        return build('docs', 'v1', credentials=creds)
    elif service == 'DRIVE':
        return build('drive', 'v3', credentials=creds)

def write_to_doc(doc_service, filename, text):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        },
    ]

    try:
        doc_service.documents().batchUpdate(documentId=filename, body={'requests': requests}).execute()
    except Exception as e:
        print(e)
        pass

def create_new_doc(service, filename):
    body = {
        "mimeType": "application/vnd.google-apps.document",
        "name": filename,
        "parents": [
            "1Ou-5cWLPXBX8kCXvqGOZeJpfUeIYJfry"
        ]
    }

    try:
        service.files().create(body=body).execute()
    except Exception as e:
        print(e)
        pass

def get_google_doc_id(service, filename):
    page_token = None
    while True:
        res = service.files().list(q=f"name='{filename}'",spaces='drive',fields='nextPageToken, files(id, name)',pageToken=page_token).execute()
        for f in res.get('files', []):
            if f.get('name') == filename:
                return f.get('id')
        page_token = res.get('nextPageToken', None)
        if page_token is None:
            break
    return None

def delete_from_doc(service, doc_id, startIdx, stopIdx):
    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': startIdx,
                    'endIndex': stopIdx
                }
            }
        },
    ]

    try:
        service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    except Exception as e:
        print(e)
        pass
