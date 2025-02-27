from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import time
from datetime import datetime
import sys

yt_dlp_path = subprocess.run("which yt-dlp", shell=True, capture_output=True, text=True).stdout.strip()
print(f"yt-dlp path found: {yt_dlp_path}", file=sys.stderr)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")  
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        # Generate a timestamped filename to ensure uniqueness
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"YouTube_Video_{current_date}.mp4")

        # yt-dlp command to download video
        command = [
  'yt-dlp',
    '--cookies-from-browser', 'chrome',  # Use cookies from Chrome directly
    '-o', video_path,
    '-f', 'best',
    video_url
        ]

        # Run download command
        subprocess.run(command, check=True)

        # Return file to the frontend for browser download history
        return send_file(video_path, as_attachment=True)

    except subprocess.CalledProcessError:
        return jsonify({"message": "Download failed"}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on port 5000
