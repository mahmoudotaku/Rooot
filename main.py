from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
import os
import uuid
import uvicorn

app = FastAPI(title="Shaytan Downloader", description="YouTube Video Downloader with Arabic Interface")

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DOWNLOAD_DIR = "downloads"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/info")
def get_video_info(url: str):
    """Extract video information including available formats"""
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Filter and format available video formats
            formats = []
            for f in info.get("formats", []):
                # Only include formats with video codec (exclude audio-only)
                if f.get("vcodec") != "none":
                    format_info = {
                        "format_id": f["format_id"],
                        "ext": f["ext"],
                        "resolution": f.get("resolution") or f"{f.get('height', 'Unknown')}p",
                        "filesize": round((f.get("filesize", 0) or 0) / 1024 / 1024, 2) if f.get("filesize") else 0
                    }
                    formats.append(format_info)
            
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "formats": formats
            }
    except Exception as e:
        return {"error": f"Failed to extract video info: {str(e)}"}

@app.get("/download")
def download_video(url: str, quality: str):
    """Download video with specified quality"""
    try:
        # Generate unique filename
        uid = str(uuid.uuid4())
        output = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")
        
        # Configure yt-dlp options
        ydl_opts = {
            "format": quality,
            "outtmpl": output,
            "quiet": True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        # Return file for download
        return FileResponse(
            file_path, 
            filename=os.path.basename(file_path),
            media_type="application/octet-stream"
        )
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}

@app.get("/cleanup")
def cleanup_downloads():
    """Clean up downloaded files from server"""
    try:
        count = 0
        for filename in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                count += 1
        return {"message": f"Cleaned up {count} files", "deleted": count}
    except Exception as e:
        return {"error": f"Cleanup failed: {str(e)}"}

@app.get("/robots.txt", response_class=HTMLResponse)
def robots_txt(request: Request):
    """Serve robots.txt for SEO"""
    domain = request.headers.get("host", "localhost:5000")
    robots_content = f"""User-agent: *
Allow: /

# السماح لجوجل بوت بالوصول لجميع الصفحات
User-agent: Googlebot
Allow: /

# منع الوصول لمجلد التحميلات
Disallow: /downloads/

# رابط خريطة الموقع
Sitemap: https://{domain}/sitemap.xml"""
    return robots_content

@app.get("/sitemap.xml", response_class=HTMLResponse)
def sitemap_xml(request: Request):
    """Serve sitemap.xml for SEO"""
    domain = request.headers.get("host", "localhost:5000")
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://{domain}/</loc>
    <lastmod>2025-09-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="ar" href="https://{domain}/" />
  </url>
</urlset>"""
    return sitemap_content

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Shaytan Downloader"}

if __name__ == "__main__":
    # Configure for Replit deployment - always use port 5000 for frontend
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
