from flask import Flask, request, jsonify
import requests
import re
import ast
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def post_message():
    rz = open("rz.txt","a", encoding="utf-8")
    data = request.json  # 假设客户端发送的是 JSON 数据
    id = data.get("id",0)
    tj = data.get("tj",0)
    le = data.get("len",0)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    utc_time = datetime.utcnow()  # 获取 UTC 时间
    china_time = utc_time + timedelta(hours=8)  # 手动调整为北京时间
    request_time = china_time.strftime('%Y-%m-%d %H:%M:%S')
    rz.write(str(client_ip)+" "+str(id)+" "+str(request_time)+"\n")
    cs = requests.get("https://service-5hxd8gip-1252368878.sh.apigw.tencentcs.com/release/query_all?id="+str(id)+"&cmd=2&platform=1011").text
    a = "".join(re.findall(r'"weaponIDList": (.*?), "',cs))
    ap = "".join(re.findall(r'"atlasPower": (.*?),',cs))
    data_list = ast.literal_eval(a)
# 获取列表长度
    length = len(data_list)
    if tj == int(ap) and le == int(length):
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
        my = "rmb="+rmb+"&bt="+bt+"&os="+str(filtered_data)
    else:
        my = "error"
    return my
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)