from flask import Flask, request, jsonify
import requests
import re
import ast

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def post_message():
    data = request.json  # 假设客户端发送的是 JSON 数据
    id = data.get("id","")
    tj = data.get("tj","")
    le = data.get("len","")
    cs = requests.get("https://service-5hxd8gip-1252368878.sh.apigw.tencentcs.com/release/query_all?id="+str(id)+"&cmd=2&platform=1011").text
    a = "".join(re.findall(r'"weaponIDList": (.*?), "',cs))
    ap = "".join(re.findall(r'"atlasPower": (.*?),',cs))
    data_list = ast.literal_eval(a)
# 获取列表长度
    length = len(data_list)
    if str(tj) == ap and str(le) == length:
        rmb ="".join(re.findall(r'"rmb": (.*?),',cs))
        bt = "".join(re.findall(r'"birthTime": (.*?),',cs))
        pattern = r'"oldDanScore":\s*(\{[^{}]*\})'
# 匹配
        match = re.search(pattern, cs)
# 提取结果
        old_dan_score = match.group(1)    
        pattern = r'"(\d+)":\s*(\d+)'
        matches = re.findall(pattern, old_dan_score)
# 将匹配结果转换为字典
        filtered_data = {key: int(value) for key, value in matches}
        my = "rmb="+rmb+"&bt="+bt+"&os="+filtered_data
    else:
        my = "0"
    return my
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)