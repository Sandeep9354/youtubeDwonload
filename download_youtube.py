from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback  # <-- Add this

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        video_url = data.get("video_url")

        if not video_url:
            return jsonify({"message": "Invalid URL"}), 400

        print(f"Received URL: {video_url}")

        # Simulating a potential issue
        # (You should replace this with your actual download logic)
        if "youtube.com" not in video_url:
            raise ValueError("Invalid YouTube URL")

        return jsonify({"message": f"Processing download for {video_url}"}), 200

    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print("\n❌ ERROR:", error_message)
        print(error_traceback)  # <-- Print full error
        return jsonify({"message": "An error occurred", "error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
