from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'static/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return jsonify({"download_url": f"/static/{info['title']}.{info['ext']}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)