from flask import Flask, render_template_string
import requests
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('TICKETMASTER_API_KEY')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
REGION = 'us-east-1'

s3 = boto3.client('s3', region_name=REGION)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>UniEvent - University Events</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f0f2f5; }
        .header { background: #1a73e8; color: white; padding: 20px; text-align: center; }
        .header h1 { margin: 0; font-size: 2em; }
        .header p { margin: 5px 0 0; opacity: 0.85; }
        .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .card img { width: 100%; height: 180px; object-fit: cover; }
        .card-body { padding: 16px; }
        .card-body h3 { margin: 0 0 8px; color: #1a73e8; font-size: 1em; }
        .card-body p { margin: 4px 0; font-size: 0.85em; color: #555; }
        .badge { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 3px 10px; border-radius: 20px; font-size: 0.75em; margin-top: 8px; }
        .footer { text-align: center; padding: 20px; color: #888; font-size: 0.85em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 UniEvent</h1>
        <p>University Events powered by AWS</p>
    </div>
    <div class="container">
        <div class="grid">
            {% for event in events %}
            <div class="card">
                {% if event.image %}
                <img src="{{ event.image }}" alt="{{ event.name }}">
                {% endif %}
                <div class="card-body">
                    <h3>{{ event.name }}</h3>
                    <p>📅 {{ event.date }}</p>
                    <p>📍 {{ event.venue }}</p>
                    <p>🏙️ {{ event.city }}</p>
                    <span class="badge">{{ event.category }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <div class="footer">UniEvent — Hosted on AWS | EC2 + S3 + ALB</div>
</body>
</html>
'''

def fetch_and_store_events():
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': API_KEY,
        'keyword': 'university',
        'size': 12,
        'countryCode': 'US'
    }
    response = requests.get(url, params=params)
    data = response.json()

    events = []
    if '_embedded' in data:
        for item in data['_embedded']['events']:
            event = {
                'name': item.get('name', 'N/A'),
                'date': item.get('dates', {}).get('start', {}).get('localDate', 'TBD'),
                'venue': item.get('_embedded', {}).get('venues', [{}])[0].get('name', 'N/A'),
                'city': item.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name', 'N/A'),
                'category': item.get('classifications', [{}])[0].get('segment', {}).get('name', 'Event'),
                'image': item.get('images', [{}])[0].get('url', '')
            }
            events.append(event)

    s3.put_object(
        Bucket=S3_BUCKET,
        Key='event-data/events.json',
        Body=json.dumps(events),
        ContentType='application/json'
    )

    return events

@app.route('/')
def index():
    try:
        events = fetch_and_store_events()
    except Exception as e:
        events = []
        print(f"Error: {e}")
    return render_template_string(HTML_TEMPLATE, events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
