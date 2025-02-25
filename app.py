from flask import Flask, request, jsonify, send_file
import requests
import re
import ast
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)

id_last_request = {}
# 限制时间间隔（1 小时）
REQUEST_INTERVAL = timedelta(hours=1)
# 缓存 ban.txt 文件内容
ban_ips = set()
if os.path.exists("ban.txt"):
    with open("ban.txt", "r", encoding="utf-8") as f:
        ban_ips = set(f.read().splitlines())

# 创建 requests 会话对象
session = requests.Session()

@app.before_request
def check_request_interval():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip in ban_ips:
        return "ban"

@app.route('/download_log')
def download_log():
    try:
        # 返回日志文件
        return send_file("rz.txt", as_attachment=True, download_name='rz.txt')
    except FileNotFoundError:
        return "Log file not found.", 404

@app.route('/ban111', methods=['POST'])
def get_message():
    global ban_ips
    data = request.json
    ip = data.get("i", "")
    with open("ban.txt", "w", encoding="utf-8") as f:
        f.write(ip)
    ban_ips = set([ip])
    return ip

@app.route('/message', methods=['POST'])
def post_message():
    data = request.json  # 假设客户端发送的是 JSON 数据
    id = data.get("id", 0)
    utc_time = datetime.utcnow()  # 获取 UTC 时间
    china_time = utc_time + timedelta(hours=8)  # 手动调整为北京时间
    if id in id_last_request:
        last_request_time = id_last_request[id]
        # 检查时间间隔
        if china_time - last_request_time < REQUEST_INTERVAL:
            return "too"  # 返回 429 状态码（请求过多）
    id_last_request[id] = china_time
    tj = data.get("tj", 0)
    le = data.get("len", 0)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    request_time = china_time.strftime('%Y-%m-%d %H:%M:%S')
    with open("rz.txt", "a", encoding="utf-8") as rz:
        rz.write(f"{client_ip} {id} {request_time}\n")

    try:
        url = f"https://service-5hxd8gip-1252368878.sh.apigw.tencentcs.com/release/query_all?id={id}&cmd=2&platform=1011"
        response = session.get(url)
        response.raise_for_status()
        cs = response.text
        json_data = json.loads(cs)
    except requests.RequestException as e:
        return f"Network error: {e}", 500
    except ValueError as e:
        return f"JSON decoding error: {e}", 500

    weapon_id_list = json_data.get("weaponIDList", [])
    atlas_power = json_data.get("atlasPower", 0)
    length = len(weapon_id_list)

    if tj == atlas_power and le == length:
        rmb = json_data.get("rmb", 0)
        birth_time = json_data.get("birthTime", 0)
        old_dan_score = json_data.get("oldDanScore", {})

        # 剔除 oldDanScore 部分数据
        pattern = r'"(\d+)":\s*(\d+)'
        old_dan_score_str = json.dumps(old_dan_score)
        matches = re.findall(pattern, old_dan_score_str)
        # 将匹配结果转换为字典
        filtered_data = {key: int(value) for key, value in matches}

        my = f"rmb={rmb}&bt={birth_time}&os={filtered_data}"
    else:
        my = "error"

    return my

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)