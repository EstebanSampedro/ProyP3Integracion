# nextcloud.py

import requests
import base64

import os
from dotenv import load_dotenv

load_dotenv()  # Esto carga las variables del archivo .env

# Ahora puedes obtener las variables de entorno
url = os.getenv('NEXTCLOUD_URL')
username = os.getenv('NEXTCLOUD_USERNAME')
password = os.getenv('NEXTCLOUD_PASSWORD')

class NextcloudService:
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        self.auth_string = base64.b64encode(f"{self.username}:{self.password}".encode()).decode('utf-8')
        self.headers = {
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.auth_string}',
        }

    def create_user(self, userid: str, password: str, email: str, displayname: str, groups=None, subadmin=None, quota=None, language=None):
        user_data = {
            "userid": userid,
            "password": password,
            "email": email,
            "displayname": displayname,
        }

        if groups:
            user_data['groups'] = groups
        if subadmin:
            user_data['subadmin'] = subadmin
        if quota:
            user_data['quota'] = quota
        if language:
            user_data['language'] = language

        operation_url = f"{self.url}/ocs/v1.php/cloud/users"

        response = requests.post(operation_url, data=user_data, headers=self.headers)
        return response

    def delete_user(self, userid: str):
        operation_url = f"{self.url}/ocs/v1.php/cloud/users/{userid}"
        response = requests.delete(operation_url, headers=self.headers)
        return response
