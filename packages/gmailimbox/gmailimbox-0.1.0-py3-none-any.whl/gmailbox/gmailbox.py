import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailBox:
    """
    A simple Gmail API client to fetch emails based on specific criteria.

    Attributes:
        service (Resource): The authenticated Google API service instance.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        """
        Initializes the GmailBox with authenticated Google API service.
        """
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def messages(self, unread=False, sent_to=None, raw=None):
        """
        Fetches messages based on the specified criteria.

        Args:
            unread (bool): If True, fetches only unread messages.
            sent_to (str): Fetches messages sent to a specific email address.
            raw (str): Additional Gmail search filter (e.g., 'has:attachment').

        Returns:
            list: A list of fetched messages.
        """
        query = []
        if unread:
            query.append('is:unread')
        if sent_to:
            query.append(f'to:{sent_to}')
        if raw:
            query.append(raw)
        query_string = ' '.join(query)
        
        results = self.service.users().messages().list(userId='me', q=query_string).execute()
        messages = results.get('messages', [])

        fetched_messages = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            fetched_messages.append(self._parse_message(msg))

        return fetched_messages

    def _parse_message(self, msg):
        """Parses the message details and returns a simplified dictionary."""
        headers = msg['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        from_email = next((header['value'] for header in headers if header['name'] == 'From'), None)

        body = ""
        if 'data' in msg['payload']['body']:
            body = base64.urlsafe_b64decode(msg['payload']['body']['data'].encode('ASCII')).decode('utf-8')
        elif 'parts' in msg['payload']:
            body = self._get_mime_part(msg['payload']['parts'])

        return {
            'subject': subject,
            'from': from_email,
            'body': body
        }

    def _get_mime_part(self, parts):
        """Recursive function to fetch the body of the email from the MIME structure."""
        text = ""
        for part in parts:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                text += base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
            elif 'parts' in part:
                text += self._get_mime_part(part['parts'])
        return text

if __name__ == '__main__':
    gmb = GmailBox()
    emails = gmb.messages(unread=True, sent_to='example@gmail.com', raw='has:attachment')
    for email in emails:
        print(email)
