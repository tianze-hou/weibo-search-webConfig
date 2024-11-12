from flask import Flask, render_template, request, jsonify
import os
import subprocess
import re
import webbrowser  # 导入webbrowser模块
import threading  # 导入threading模块

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.json

    # 读取当前的settings.py内容
    with open('weibo/settings.py', 'r', encoding='utf-8') as f:
        settings_content = f.read()

    # 使用正则表达式替换配置项
    settings_content = re.sub(r'^DEFAULT_REQUEST_HEADERS = \{.*?\}', 
                              "DEFAULT_REQUEST_HEADERS = {\n    'Accept':\n    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\n    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',\n    'cookie': '" + data['cookie'] + "'\n}", 
                              settings_content, flags=re.DOTALL | re.MULTILINE)
    
    keywords = [f"'{keyword}'" for keyword in data['keywords']]
    settings_content = re.sub(r'^KEYWORD_LIST = .*$', f"KEYWORD_LIST = [{', '.join(keywords)}]", settings_content, flags=re.MULTILINE)
    settings_content = re.sub(r'^START_DATE = .*$', f"START_DATE = '{data['start-date']}'", settings_content, flags=re.MULTILINE)
    settings_content = re.sub(r'^END_DATE = .*$', f"END_DATE = '{data['end-date']}'", settings_content, flags=re.MULTILINE)
    settings_content = re.sub(r'^WEIBO_TYPE = .*$', f"WEIBO_TYPE = {data['weibo-type']}", settings_content, flags=re.MULTILINE)
    settings_content = re.sub(r'^CONTAIN_TYPE = .*$', f"CONTAIN_TYPE = {data['contain-type']}", settings_content, flags=re.MULTILINE)
    settings_content = re.sub(r'^FURTHER_THRESHOLD = .*$', f"FURTHER_THRESHOLD = {data['threshold']}", settings_content, flags=re.MULTILINE)

    pipelines = []
    pipelines.append("'weibo.pipelines.DuplicatesPipeline': 300")
    if data.get('save-csv', False):
        pipelines.append("'weibo.pipelines.CsvPipeline': 301")
    if data.get('save-mongodb', False):
        pipelines.append("'weibo.pipelines.MongoPipeline': 303")
    if data.get('save-mysql', False):
        pipelines.append("'weibo.pipelines.MysqlPipeline': 302")
    pipelines_str = ",\n    ".join(pipelines)
    if not pipelines:
        settings_content = re.sub(r'^ITEM_PIPELINES = \{.*?\}', "ITEM_PIPELINES = {}", settings_content, flags=re.DOTALL | re.MULTILINE)
    else:
        settings_content = re.sub(r'^ITEM_PIPELINES = \{.*?\}', f"ITEM_PIPELINES = {{\n    {pipelines_str}\n}}", settings_content, flags=re.DOTALL | re.MULTILINE)

    if data['save-mongodb']:
        settings_content = re.sub(r'^MONGO_URI = .*$', f"MONGO_URI = '{data['mongo-url']}'", settings_content, flags=re.MULTILINE)
    else:
        settings_content = re.sub(r'^MONGO_URI = .*$', "# MONGO_URI = 'localhost'", settings_content, flags=re.MULTILINE)

    if data['save-mysql']:
        settings_content = re.sub(r'^MYSQL_HOST = .*$', f"MYSQL_HOST = '{data['mysql-host']}'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_PORT = .*$', f"MYSQL_PORT = {data['mysql-port']}", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_USER = .*$', f"MYSQL_USER = '{data['mysql-user']}'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_PASSWORD = .*$', f"MYSQL_PASSWORD = '{data['mysql-password']}'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_DATABASE = .*$', f"MYSQL_DATABASE = '{data['mysql-database']}'", settings_content, flags=re.MULTILINE)
    else:
        settings_content = re.sub(r'^MYSQL_HOST = .*$', "# MYSQL_HOST = 'localhost'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_PORT = .*$', "# MYSQL_PORT = 3306", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_USER = .*$', "# MYSQL_USER = 'root'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_PASSWORD = .*$', "# MYSQL_PASSWORD = '123456'", settings_content, flags=re.MULTILINE)
        settings_content = re.sub(r'^MYSQL_DATABASE = .*$', "# MYSQL_DATABASE = 'weibo'", settings_content, flags=re.MULTILINE)

    # 写回settings.py
    with open('weibo/settings.py', 'w', encoding='utf-8') as f:
        f.write(settings_content)

    return jsonify({'status': 'success'})

@app.route('/start_crawl', methods=['POST'])
def start_crawl():
    project_name = request.json['project-name']
    command = f"scrapy crawl search -s JOBDIR=crawls/{project_name}"
    subprocess.Popen(command, shell=True)
    return jsonify({'status': 'started'})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # 在新线程中打开浏览器
    app.run(debug=False)
