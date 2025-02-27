from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import shutil
from datetime import datetime

# Find yt-dlp path dynamically
yt_dlp_path = shutil.which("yt-dlp")

if yt_dlp_path:
    print(f"yt-dlp found at: {yt_dlp_path}")
else:
    print("yt-dlp not found. Make sure it's installed and added to PATH.")

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = os.path.expanduser('/opt/render/project/src/downloads')  # Ensure correct path
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"YouTube_Video_{current_date}.mp4")

        print(f"Downloading video from: {video_url}")  # Debugging print

        command = [
            yt_dlp_path,  # Use detected path
            '-o', video_path,  
            '-f', 'best',
            video_url
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print("yt-dlp Error:", result.stderr)
            return jsonify({"message": "Download failed", "error": result.stderr}), 500

        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
