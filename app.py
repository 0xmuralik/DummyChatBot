from flask import Flask, render_template, request
from talk import chatbot_response

 
app = Flask(__name__)


@app.route("/")
def home():
    #return "Hello World!"
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot_response(userText))

 
if __name__ == "__main__":
    app.run()