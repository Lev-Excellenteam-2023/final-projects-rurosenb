import asyncio
import os
import requests
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import sqlite3

load_dotenv()

@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == 'done'

class WebAppClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path, email=None):
        upload_url = f"{self.base_url}/upload"
        try:
            with open(file_path, 'rb') as file:
                data = {'email': email} if email else {}
                response = requests.post(upload_url, files={'file': file}, data=data)
                response.raise_for_status()
                data = response.json()
                return data['uid']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Upload failed: {e}")

    def status(self, uid):
        status_url = f"{self.base_url}/status/{uid}"
        try:
            response = requests.get(status_url)
            response.raise_for_status()
            data = response.json()
            timestamp = datetime.utcfromtimestamp(data['timestamp'])
            return Status(data['status'], data['filename'], timestamp, data['explanation'])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Status retrieval failed: {e}")

# Example usage
if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1:5000"
    client = WebAppClient(BASE_URL)

    try:
        # Upload a file
        file_path = "C:/targilim/Ruty-Presentation.pptx"
        email = "user@example.com"  # Optional email parameter
        uid = client.upload(file_path, email=email)
        print(f"Uploaded successfully. UID: {uid}")

        # Check status
        status_obj = client.status(uid)
        if status_obj.is_done():
            print("Processing is done!")
            print(f"Filename: {status_obj.filename}")
            print(f"Timestamp: {status_obj.timestamp}")
            print(f"Explanation: {status_obj.explanation}")
        else:
            print("Processing is still pending.")
    except Exception as e:
        print(f"An error occurred: {e}")
