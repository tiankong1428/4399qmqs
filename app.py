from flask import Flask, request, jsonify
import requests
import re
import ast
from datetime import datetime, timedelta
import os

app = Flask(__name__)

id_last_request = {}

# 限制时间间隔（1 小时）
REQUEST_INTERVAL = timedelta(hours=1)

@app.before_request
def check_request_interval():
    if os.path.exists("ban.txt"):
        ban = open("ban.txt","r",encoding="utf-8").read()
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip in ban:
            return "ban"
@app.route('/download_log')
def download_log():
    try:
        # 返回日志文件
        return send_file(LOG_FILE, as_attachment=True, download_name='rz.txt')
    except FileNotFoundError:
        return "Log file not found.", 404
@app.route('/ban111', methods=['POST'])
def get_message():
    data = request.json
    ip = data.get("i","")
    ban = open("ban.txt","w", encoding="utf-8")
    ban.write(ip)
    ban.close()
    return ip
@app.route('/message', methods=['POST'])
def post_message():
    
    rz = open("rz.txt","a", encoding="utf-8")
    data = request.json  # 假设客户端发送的是 JSON 数据
    id = data.get("id",0)
    utc_time = datetime.utcnow()  # 获取 UTC 时间
    china_time = utc_time + timedelta(hours=8)  # 手动调整为北京时间
    if id in id_last_request:
        last_request_time = id_last_request[id]
        # 检查时间间隔
        if current_time - last_request_time < REQUEST_INTERVAL:
            return "too", 429  # 返回 429 状态码（请求过多）
    id_last_request[id] = current_time
    tj = data.get("tj",0)
    le = data.get("len",0)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
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