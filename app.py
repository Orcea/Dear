from flask import Flask, render_template, request, jsonify, send_file
import random
import os

app = Flask(__name__)

messages = []

@app.route("/")
def index():
    phrases = ["Good luck!", "Have a nice day!", "How are you today?", "I like banana", "im espanol", "who is DearChat?", "Im cool"]
    return render_template("index.html", random_phrase=random.choice(phrases))

@app.route("/chat/<username>")
def chat(username):
    return render_template("chat.html", username=username)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    username = request.form.get("username")
    # audio_blob = request.files["audioBlob"]
    print(request.files)
    if message and username:
        messages.append({"user": username, "message": message})
        
        # Удаляем старые сообщения, если их больше 10
        if len(messages) > 10:
            messages.pop(0)

    # if message and username and audio_blob:
    #     # Сохраняем аудио-файл на сервер
    #     audio_path = os.path.join("audio", f"{random.randint(1, 1000000)}.wav")
    #     audio_blob.save(audio_path)
        
        # Добавляем сообщение с ссылкой на аудио
        messages.append({"user": username, "message": message, "audio": audio_path})
        
        # Удаляем старые сообщения, если их больше 10
        if len(messages) > 10:
            messages.pop(0)
    
    return jsonify({"status": "OK"})

@app.route("/send_audio_message", methods=["POST"])
def send_audio_message():
    message = request.form.get("message")
    username = request.form.get("username")
    audio_blob = request.files["audio"]
    
    if message and username and audio_blob:
        # Сохраняем аудио-файл на сервер
        audio_path = os.path.join("audio", f"{random.randint(1, 1000000)}.wav")
        audio_blob.save(audio_path)
        
        # Добавляем сообщение с ссылкой на аудио
        messages.append({"user": username, "message": message, "audio": audio_path})
        
        # Удаляем старые сообщения, если их больше 10
        if len(messages) > 10:
            messages.pop(0)
    
    return jsonify({"status": "OK"})

@app.route("/get_messages")
def get_messages():
    message_html = ""
    for message in messages:
        message_html += f"<p>{message['user']}: {message['message']}</p>"
        if 'audio' in message:
            audio_path = message['audio']
            message_html += f'<audio controls><source src="{audio_path}" type="audio/wav"></audio>'
    return message_html

if __name__ == "__main__":
    app.run(debug=True)
