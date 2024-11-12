document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit();
    const dateOptions = {
        format: 'yyyy-mm-dd',
        defaultDate: new Date(),
        setDefaultDate: true,
        autoClose: true,
        i18n: {
            months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            monthsShort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            weekdays: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            weekdaysShort: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
            weekdaysAbbrev: ['日', '一', '二', '三', '四', '五', '六'],
            done: '确定',
            clear: '清除',
            cancel: '取消'
        }
    };
    M.Datepicker.init(document.querySelectorAll('.datepicker'), dateOptions);
    M.FormSelect.init(document.querySelectorAll('select'), {});

    // 添加关键词
    document.querySelector('.add-keyword').addEventListener('click', function() {
        const container = document.getElementById('keywords-container');
        const newKeyword = document.createElement('div');
        newKeyword.className = 'keyword-input input-field';
        newKeyword.innerHTML = `
            <input type="text" class="keyword" required>
            <label>搜索关键词</label>
            <button class="btn-floating waves-effect waves-light red remove-keyword">
                <i class="material-icons">remove</i>
            </button>
        `;
        container.appendChild(newKeyword);
        M.updateTextFields();
    });

    // 移除关键词
    document.getElementById('keywords-container').addEventListener('click', function(e) {
        if (e.target.closest('.remove-keyword')) {
            e.target.closest('.keyword-input').remove();
        }
    });

    // 勾选“保存到MongoDB”显示配置
    document.getElementById('save-mongodb').addEventListener('change', function() {
        document.getElementById('mongodb-config').style.display = this.checked ? 'block' : 'none';
    });

    // 勾选“保存到MySQL”显示配置
    document.getElementById('save-mysql').addEventListener('change', function() {
        document.getElementById('mysql-config').style.display = this.checked ? 'block' : 'none';
    });

    // 触发开始运行按钮
    document.getElementById('start-btn').addEventListener('click', function() {
        // 收集表单数据
        const projectName = document.getElementById('project-name').value.trim();
        const cookie = document.getElementById('cookie').value.trim();
        
        if (!projectName) {
            M.toast({html: '请填写项目名称', classes: 'red'});
            return;
        }

        if (!cookie) {
            M.toast({html: '请填写Cookie', classes: 'red'});
            return;
        }

        const keywordElements = document.querySelectorAll('.keyword');
        const keywords = [];
        keywordElements.forEach(el => {
            const kw = el.value.trim();
            if (kw) {
                keywords.push(kw);
            }
        });

        if (keywords.length === 0) {
            M.toast({html: '请添加至少一个关键词', classes: 'red'});
            return;
        }

        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const weiboType = document.getElementById('weibo-type').value;
        const containType = document.getElementById('contain-type').value;
        const saveCsv = document.getElementById('save-csv').checked;
        const saveMongodb = document.getElementById('save-mongodb').checked;
        const mongoUrl = document.getElementById('mongo-url').value.trim();
        const saveMysql = document.getElementById('save-mysql').checked;
        const mysqlHost = document.getElementById('mysql-host').value.trim();
        const mysqlPort = document.getElementById('mysql-port').value.trim();
        const mysqlUser = document.getElementById('mysql-user').value.trim();
        const mysqlPassword = document.getElementById('mysql-password').value.trim();
        const mysqlDatabase = document.getElementById('mysql-database').value.trim();
        const threshold = document.getElementById('threshold').value;

        // 构建发送的数据对象
        const data = {
            'project-name': projectName,
            'cookie': cookie,
            'keywords': keywords,
            'start-date': startDate,
            'end-date': endDate,
            'weibo-type': weiboType,
            'contain-type': containType,
            'save-csv': saveCsv,
            'save-mongodb': saveMongodb,
            'mongo-url': mongoUrl,
            'save-mysql': saveMysql,
            'mysql-host': mysqlHost,
            'mysql-port': mysqlPort,
            'mysql-user': mysqlUser,
            'mysql-password': mysqlPassword,
            'mysql-database': mysqlDatabase,
            'threshold': threshold
        };

        // 发送保存配置的请求
        fetch('/save_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                M.toast({html: '配置已保存', classes: 'green'});
                // 发送启动爬取的请求
                return fetch('/start_crawl', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({'project-name': projectName})
                });
            } else {
                throw new Error('保存配置失败');
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'started') {
                M.toast({html: '爬取任务已启动，请在命令行窗口继续', classes: 'green'});
            } else {
                throw new Error('启动爬取任务失败');
            }
        })
        .catch(error => {
            console.error(error);
            M.toast({html: '发生错误: ' + error.message, classes: 'red'});
        });
    });

    // 初始化模态框
    M.Modal.init(document.querySelectorAll('.modal'), { dismissible: true, opacity: 0.5 });
});
