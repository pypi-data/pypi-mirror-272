import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Optional, Dict, Any

class GmailBox:
    def __init__(self):
        self.request = requests.session()
        self.headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.request.get('https://www.emailnator.com/', headers=self.headers)
        self.token = unquote(self.request.cookies.get_dict()['XSRF-TOKEN'])
        self.headers["x-xsrf-token"] = self.token
        self.email = ""

    def new_email(self) -> Dict[str, str]:
        json_data = {'email': ['dotGmail']}
        response = self.request.post('https://www.emailnator.com/generate-email', headers=self.headers, json=json_data).json()
        self.email = response['email'][0]
        return {'email': self.email}

    def inbox(self, email: Optional[str] = None) -> Dict[str, Any]:
        email = email or self.email
        time.sleep(0.20)
        json_data = {'email': email}
        response = self.request.post('https://www.emailnator.com/message-list', headers=self.headers, json=json_data).json()
        messages = []
        for item in response['messageData'][1:]:
            messageID = item['messageID']
            json_data = {'email': email, 'messageID': messageID}
            response = self.request.post('https://www.emailnator.com/message-list', headers=self.headers, json=json_data).text
            soup = BeautifulSoup(response, 'html.parser')
            message = soup.text.strip()
            try:
                tim, message = re.search(r"Time:\s*\n\s*\n(.+?)([\s\S]+)", message).groups()
            except:
                pass
            sender = item['from']
            email_sender = re.findall(r'<(.*?)>', sender)[0] if re.findall(r'<(.*?)>', sender) else sender
            sender_name = re.findall(r'"(.*?)"', sender)[0] if re.findall(r'"(.*?)"', sender) else sender.split(f'<{email_sender}>')[0]
            messages.append({'from': sender_name, 'email': email_sender, 'subject': item['subject'], 'message': message.strip(), 'time': item['time']})
        return messages