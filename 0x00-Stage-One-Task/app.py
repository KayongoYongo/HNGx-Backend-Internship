#!/usr/bin/python3
"""The endpoint should take two GET request query parameters
and return specific information in JSON format.
"""

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
    github_file_url = f"{github_repo_url}/blob/master/0x00-Stage-One-Task/app.py"

    # format for the response data
    response_data = {
        "slack_name": slack_name,
        "current_day": current_day,
        "utc_time": utc_time,
        "track": track,
        "github_file_url": github_file_url,
        "github_repo_url": github_repo_url,
        "status_code": 200
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
