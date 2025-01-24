from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = pickle.load(open('token.json', 'rb'))
    if not creds or creds.expired or creds.refresh.token is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=8000)
        pickle.dump(creds, open('token.json', 'wb'))
    return build('calendar', 'v3', credentials=creds)

@app.route('/')
def index():
    service = get_google_calendar_service()
    events_result = service.events().list(calendarId='primary', timeMin='2025-01-24T00:00:00Z',
                                          maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events.result.get('items', [])

    available slots = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        available_slots.append({
            'summary': event['summary'],
            'start': start
        })

    return render_template('index.html', available_slots=available_slots)

@app.route('/book/<event_id>', methods=['GET', 'POST'])
def book(event_id):
    if request.method == 'POST':
        patient_data = {
            'full_name': request.form['full_name'],
            'age': request.form['age']
            'dob': request.form['dob']
            'phone': request.form['phone']
            'email': request.form['email']
            'address': request.form['address']
            'rg': request.form['rg']
            'cpf': request.form['cpf']
        }

#Send confirmation (WhatsApp/email integration should be added here)

    return redirect(url_for('confirmation'))

    return render_template('book.html', event_id=event_id)

@app.route('/confirmation')
def confirmation():
    return "Your appointment is confirmed!"

if __name__ == '__main__':
    app.run(debug=True)
    
