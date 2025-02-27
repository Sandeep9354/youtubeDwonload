from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Define download folder
DOWNLOAD_FOLDER = os.path.expanduser(r'C:\Users\kumar\Downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        # Generate a timestamped filename
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"YouTube_Video_{current_date}.mp4")

        # yt-dlp command
        command = [
            'yt-dlp',
            '--cookies-from-browser', 'chrome',  # Automatically fetch cookies from Chrome
            '-o', video_path,
            '-f', 'bv+ba/b',
            video_url
        ]

        # Run the command and capture errors
        result = subprocess.run(command, capture_output=True, text=True)

        # Log output for debugging
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Check if download failed
        if result.returncode != 0:
            return jsonify({"message": "Download failed", "error": result.stderr}), 500

        # Return file to frontend
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on port 5000
