from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp, os, uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/info")
def get_video_info(url: str):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [{
            "format_id": f["format_id"],
            "ext": f["ext"],
            "resolution": f.get("resolution") or f"{f.get('height', '')}p",
            "filesize": round((f.get("filesize", 0) or 0) / 1024 / 1024, 2)
        } for f in info.get("formats", []) if f.get("vcodec") != "none"]
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        }

@app.get("/download")
def download(url: str, quality: str):
    uid = str(uuid.uuid4())
    output = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")
    ydl_opts = {"format": quality, "outtmpl": output, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    return FileResponse(file_path, filename=os.path.basename(file_path))

@app.get("/cleanup")
def clean():
    count = 0
    for f in os.listdir(DOWNLOAD_DIR):
        os.remove(os.path.join(DOWNLOAD_DIR, f))
        count += 1
    return {"deleted": count}
