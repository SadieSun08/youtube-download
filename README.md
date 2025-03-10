# YouTube 视频下载器

一个简单的 YouTube 视频下载网站，使用 FastAPI + Jinja2 + yt-dlp + TailwindCSS 构建。

## 功能特点

- 支持输入 YouTube 视频链接进行下载
- 异步下载处理，避免阻塞
- 下载进度提示
- 视频信息展示（标题、时长、作者、描述、文件大小）
- 支持在线预览已下载的视频
- 响应式设计，支持移动端访问

## 安装步骤

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行应用

执行以下命令启动应用：
```bash
python run.py
```

启动后访问 http://localhost:8000 即可使用。

## 目录结构

```
.
├── main.py              # 主应用程序文件
├── run.py              # 启动脚本
├── requirements.txt     # 项目依赖
├── static/             # 静态文件目录
│   ├── videos/         # 下载的视频存储目录
│   └── css/           # CSS 文件目录
└── templates/          # 模板文件目录
    └── index.html     # 主页面模板
```

## 注意事项

- 确保有足够的磁盘空间存储下载的视频
- 建议使用虚拟环境运行应用
- 需要稳定的网络连接以确保视频下载顺利完成 