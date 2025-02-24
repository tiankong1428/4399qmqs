from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def post_message():
    data = request.json  # 假设客户端发送的是 JSON 数据
    id = data.get("id","")
    tj = data.get("tj","")
    cs = requests.get("https://service-5hxd8gip-1252368878.sh.apigw.tencentcs.com/release/query_all?id="+str(id)+"&cmd=2&platform=1011").text
    my ="".join(re.findall(r'"rmb": (.*?),',cs))
    return my
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)