#!/usr/bin/python3

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_information():
    slack_name = request.args.get('slack_name')
    track = request.args.get('track')

    if not slack_name or not track:
        return jsonify({"error": "slack_name and track parameters are required"}), 400

    # Get current UTC time with a +/-2 minute window
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    utc_time = utc_now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Get the current day of the week
    current_day = utc_now.strftime('%A')

    # Construct GitHub URLs
    github_repo_url = "https://github.com/KayongoYongo/HNGx-Backend-Internship"
    github_file_url = "

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
