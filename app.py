from flask import Flask

app = Flask(__name__)

@app.route('/message', methods=['GET'])
def get_message():
    return "这是一个通过 GET 请求返回的消息。"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)