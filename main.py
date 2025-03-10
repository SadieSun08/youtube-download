from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import yt_dlp
import os
import asyncio
import humanize
from datetime import datetime
import aiofiles
import json

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板
templates = Jinja2Templates(directory="templates")

# 视频下载目录
VIDEOS_DIR = "static/videos"
VIDEOS_INFO_FILE = "static/videos/video_info.json"

# 确保目录存在
os.makedirs(VIDEOS_DIR, exist_ok=True)

# 初始化视频信息文件
if not os.path.exists(VIDEOS_INFO_FILE):
    with open(VIDEOS_INFO_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_video_info():
    try:
        with open(VIDEOS_INFO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_video_info(info):
    with open(VIDEOS_INFO_FILE, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

@app.get("/")
async def home(request: Request):
    videos = load_video_info()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "videos": videos}
    )

@app.post("/download")
async def download_video(url: str = Form(...)):
    try:
        # yt-dlp配置
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(VIDEOS_DIR, '%(title)s.%(ext)s'),
            'quiet': True,
            # 添加以下配置来处理限制
            'nocheckcertificate': True,
            'no_warnings': False,
            'extract_flat': True,
            'ignoreerrors': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        }
        
        # 获取视频信息
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise Exception("无法获取视频信息")
                
            video_title = info['title']
            filename = ydl.prepare_filename(info)
            
            # 更新下载配置
            ydl_opts.update({
                'format': 'best',
                'extract_flat': False,
            })
            
            # 使用新配置下载视频
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 获取文件大小
            file_size = os.path.getsize(filename)
            
            # 准备视频信息
            video_info = {
                'title': info['title'],
                'duration': str(datetime.fromtimestamp(info['duration']).strftime('%H:%M:%S')) if 'duration' in info else 'Unknown',
                'author': info.get('uploader', 'Unknown'),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else 'No description',
                'file_size': humanize.naturalsize(file_size),
                'local_path': os.path.relpath(filename, 'static'),
                'download_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 更新视频信息文件
            videos = load_video_info()
            videos.append(video_info)
            save_video_info(videos)
            
            return JSONResponse({
                "status": "success",
                "message": "下载完成",
                "video_info": video_info
            })
            
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=400) 