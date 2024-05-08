import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote


class GmailBox:
    def __init__(self):
        self.request = requests.session()
        headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.request.get('https://www.emailnator.com/', headers=headers)
        self.token = unquote(self.request.cookies.get_dict()['XSRF-TOKEN'])

    def new_email(self):
        headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-xsrf-token': f'{self.token}',
        }
        json_data = {
            'email': [
                'dotGmail',
            ],
        }
        response = self.request.post('https://www.emailnator.com/generate-email', headers=headers, json=json_data).json()
        self.email = response['email'][0]
        return {'email': self.email}

    def inbox(self, email=None):
        if email is None:
            email = self.email
        time.sleep(0.20)
        headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-xsrf-token': f'{self.token}',
        }
        json_data = {
            'email': f'{email}',
        }
        response = self.request.post('https://www.emailnator.com/message-list', headers=headers, json=json_data).json()
        hamo = []
        for index, item in enumerate(response['messageData']):
            if index == 0:
                continue
            hamo.append(item)
        end = []
        for hamoo in hamo:
            messageID = hamoo['messageID']
            json_data = {
                'email': f'{email}',
                'messageID': f'{messageID}',
            }
            response = self.request.post('https://www.emailnator.com/message-list', headers=headers, json=json_data).text

            soup = BeautifulSoup(response, 'html.parser')
            formatted_html = soup.prettify()
            soup = BeautifulSoup(formatted_html, 'html.parser')
            try:
                tim = re.search(r"Time:\s*\n\s*\n(.+)", soup.text.strip()).group(1)
                message = (soup.text.strip().split(f'{tim}',1)[1]).strip()
            except:
                message = soup.text.strip()
            sender = hamoo['from']
            try:
                email_sender = re.findall(r'<(.*?)>', sender)[0]
            except:
                email_sender = sender
            try:
                sender_name = re.findall(r'"(.*?)"', sender)[0]
            except:
                sender_name = sender.split(f'<{email_sender}>')[0]
            subject = hamoo['subject']
            time_sent = hamoo['time']
            end.append({'from': sender_name, 'email': email_sender, 'subject': subject, 'message': message, 'time': time_sent})
        return end
