# weibo-search webConfig

weibo-search webConfig 是一个基于 [dataabc/weibo-search](https://github.com/dataabc/weibo-search) 的可视化微博爬虫配置工具。

[点击跳转至快速开始](#快速开始)


## 功能

- **关键词搜索**: 连续获取一个或多个微博关键词的搜索结果，可以指定时间范围。支持获得几乎全部的相关搜索结果。
- **数据保存**: 
  - 写入 **csv文件**（默认）
  - 写入 **MySQL数据库**（可选）
  - 写入 **MongoDB数据库**（可选）
- **输出信息**:
  - 包括微博ID、内容、发布时间、点赞数、转发数、评论数等详细信息。
- **进度同步**: 使用相同的项目名称，可以同步过往的爬虫进度，避免重复爬取相同的微博。

## 输出内容
- 微博id：微博的id，为一串数字形式
- 微博bid：微博的bid
- 微博内容：微博正文
- 头条文章url：微博中头条文章的url，若某微博中不存在头条文章，则该值为''
- 原始图片url：原创微博图片和转发微博转发理由中图片的url，若某条微博存在多张图片，则每个url以英文逗号分隔，若没有图片则值为''
- 视频url: 微博中的视频url和Live Photo中的视频url，若某条微博存在多个视频，则每个url以英文分号分隔，若没有视频则值为''
- 微博发布位置：位置微博中的发布位置
- 微博发布时间：微博发布时的时间，精确到天
- 点赞数：微博被赞的数量
- 转发数：微博被转发的数量
- 评论数：微博被评论的数量
- 微博发布工具：微博的发布工具，如iPhone客户端、HUAWEI Mate 20 Pro等，若没有则值为''
- 话题：微博话题，即两个#中的内容，若存在多个话题，每个url以英文逗号分隔，若没有则值为''
- @用户：微博@的用户，若存在多个@用户，每个url以英文逗号分隔，若没有则值为''
- 原始微博id：为转发微博所特有，是转发微博中那条被转发微博的id，那条被转发的微博也会存储，字段和原创微博一样，只是它的本字段为空
- 结果文件：保存在当前目录“结果文件”文件夹下以关键词为名的文件夹里
- user_authentication：微博用户类型，值分别是`蓝v`，`黄v`，`红v`，`金v`和`普通用户`

## 快速开始

1. 克隆本仓库到本地：

   ```bash
   git clone https://github.com/yourusername/weibo-search-webconfig.git
   ```

2. 进入项目目录：

   ```bash
   cd weibo-search-webconfig
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用程序：

   ```bash
   python app.py
   ```

5. 在浏览器中打开 [http://127.0.0.1:5000](http://127.0.0.1:5000) 访问界面进行配置和运行。

6. 爬虫启动后可关闭页面，**但须保持命令行界面开启**。

## 结果文件

爬虫结果将保存在 `结果文件/{爬取的关键词}` 目录下。

## 进度记录

爬虫的历史记录将保存在 `crawls/{项目名称}` 目录中，这样你可以在项目名称相同的情况下同步过往的爬虫进度，避免重复爬取相同的微博。

## 使用说明

所有配置在 `setting.py` 文件中完成，该文件位于 “weibo-search\weibo\settings.py”。**正常使用可视化配置的情况下不需要打开文件进行手动配置**。具体配置项可参考原项目[dataabc/weibo-search](https://github.com/dataabc/weibo-search)。

### 获取 Cookie

1. 使用 Chrome 浏览器打开 [weibo.com](https://weibo.com/) 并登录。
2. 按 F12 打开开发者工具，找到 Network → weibo.com → Headers → Request Headers，复制 "Cookie:" 后的值。
3. 将上述 Cookie 值粘贴到应用程序的 Cookie 设置中。

## 数据库配置

- **MongoDB**: 可在界面中输入 MONGO_URL。
- **MySQL**: 需配置 MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD 和 MYSQL_DATABASE。

## todo

- [x] 不要让浏览器误以为这是个可以保存的密码 🔒
- [ ] 支持下载图片和视频 🌄
- [ ] 在界面中显示日志 📔
- [ ] 在界面中显示爬虫进度可视化 📈
- [ ] 封装成可执行程序 💻

## 许可

此项目基于MIT许可证开源 - 详情参见[LICENSE](LICENSE)文件。

生生不息，繁荣昌盛。
