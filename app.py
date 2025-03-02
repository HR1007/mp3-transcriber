from flask import Flask, request, jsonify, render_template
from googletrans import Translator
import warnings
import whisper
import socket
import os
import webbrowser
import time

def open_browser():
    time.sleep(1)  # 確保 Flask 先啟動
    webbrowser.open("http://127.0.0.1:5001")

warnings.filterwarnings("ignore", category=UserWarning)


#請先手動進入虛擬環境
#使用套件
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 允許所有請求

model = whisper.load_model("small")
translator = Translator()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No selected file"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 🎙️ Whisper 語音辨識
    result = model.transcribe(filepath)
    text = result["text"]

     # 🌍 Google 翻譯（德文 → 繁體中文）
    translated_text = translator.translate(text, src="de", dest="zh-tw").text
    
    os.remove(filepath)

    return jsonify({
        "transcription": text,
        "translation": translated_text
    })

import socket

def find_available_port():
    """ 自動尋找可用的端口 """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == "__main__":
    port = find_available_port()  # 自動尋找可用端口
    url = f"http://127.0.0.1:{port}"  # 生成對應的網址
    
    # 讓 Flask 在啟動後自動開啟瀏覽器
    webbrowser.open(url)
    
    app.run(debug=False, host="127.0.0.1", port=port)



