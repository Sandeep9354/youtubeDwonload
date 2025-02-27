import subprocess
import os
from flask import Flask, request, send_file, jsonify
from datetime import datetime

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.expanduser("~/Downloads")  # Change this path if needed
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"message": "Invalid URL"}), 400

    try:
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_path = os.path.join(DOWNLOAD_FOLDER, f"YouTube_Video_{current_date}.mp4")

        command = [
            "yt-dlp",
            "--cookies-from-browser", "chrome",  # Use Chrome cookies for authentication
            "-o", video_path,
            "-f", "bv+ba/b",
            video_url
        ]

        # Run command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)  # Print standard output for debugging
        print("STDERR:", result.stderr)  # Print error output for debugging

        if result.returncode != 0:
            return jsonify({"message": "Download failed", "error": result.stderr}), 500

        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
