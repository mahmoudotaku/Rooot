# YouTube Downloader - تحميل الفيديوهات

تطبيق ويب لتحميل فيديوهات YouTube بواجهة عربية وخيارات جودة متعددة.

## المميزات

- ✅ واجهة عربية كاملة
- ✅ تحميل بجودات مختلفة (720p, 480p, 360p, audio only)
- ✅ عرض معلومات الفيديو والصورة المصغرة
- ✅ تصميم عصري ومتجاوب
- ✅ تنظيف الملفات المؤقتة تلقائياً

## كيفية التشغيل

### التشغيل المحلي

1. استنسخ المستودع:
```bash
git clone https://github.com/[username]/youtube-downloader
cd youtube-downloader
```

2. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. تشغيل التطبيق:
```bash
python main.py
```

4. افتح المتصفح على: `http://localhost:8000`

### التشغيل على Replit

[![Run on Repl.it](https://replit.com/badge/github/[username]/youtube-downloader)](https://replit.com/@[username]/youtube-downloader)

## بنية المشروع

```
├── main.py              # الملف الرئيسي للخادم
├── templates/
│   └── index.html       # صفحة الويب الرئيسية
├── static/
│   ├── style.css        # ملف التنسيق
│   └── script.js        # ملف JavaScript
├── downloads/           # مجلد التحميلات المؤقت
├── requirements.txt     # متطلبات Python
└── README.md           # هذا الملف
```

## التقنيات المستخدمة

- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **YouTube Downloader**: yt-dlp
- **Template Engine**: Jinja2

## المساهمة

مرحب بالمساهمات! يرجى فتح Issue أو Pull Request.

## الترخيص

هذا المشروع مفتوح المصدر تحت رخصة MIT.