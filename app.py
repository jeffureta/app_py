from flask import Flask, request, render_template, redirect
import sqlite3
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

def download_db_from_drive():
    creds = Credentials.from_service_account_file('/Users/jeffureta/repos/app_py/test-373321-cfe72a2ca785.json', scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build('drive', 'v3', credentials=creds)

    file_id = '1VwWbYQvEZeATgdNvfOfjKYO7OA8xKA1O'
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO('example.db', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

def upload_db_to_drive():
    creds = Credentials.from_service_account_file('/Users/jeffureta/repos/app_py/test-373321-cfe72a2ca785.json', scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build('drive', 'v3', credentials=creds)

    file_id = '1VwWbYQvEZeATgdNvfOfjKYO7OA8xKA1O'

    # Create a MediaFileUpload object and specify the file's MIME type
    media = MediaFileUpload('example.db', mimetype='application/x-sqlite3')

    # Update the file on Google Drive
    request = drive_service.files().update(media_body=media, fileId=file_id)
    request.execute()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    download_db_from_drive()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()

        upload_db_to_drive()  # Upload the modified DB back to Google Drive

        return redirect('/')

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
