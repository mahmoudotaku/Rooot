# Shaytan Downloader Pro - YouTube Video Downloader

## نظرة عامة
تطبيق ويب لتحميل فيديوهات YouTube بواجهة عربية كاملة وتحسينات SEO للبحث العربي.

## التقنيات المستخدمة
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **تحميل الفيديوهات**: yt-dlp
- **قوالب**: Jinja2
- **إدارة التبعيات**: uv (Python)

## المميزات الرئيسية
- ✅ واجهة عربية كاملة (RTL)
- ✅ تحميل بجودات مختلفة (720p, 480p, 360p)
- ✅ تصميم عصري ومتجاوب
- ✅ تحسينات SEO للبحث العربي
- ✅ ملفات robots.txt و sitemap.xml
- ✅ meta tags محسنة
- ✅ تنظيف الملفات المؤقتة

## بنية المشروع
```
├── main.py              # خادم FastAPI الرئيسي
├── templates/
│   └── index.html       # الصفحة الرئيسية
├── static/
│   ├── style.css        # التنسيقات
│   ├── script.js        # JavaScript
│   ├── robots.txt       # ملف الروبوتات
│   └── sitemap.xml      # خريطة الموقع
├── downloads/           # مجلد التحميلات المؤقت
├── pyproject.toml       # تبعيات Python
└── uv.lock             # ملف القفل للتبعيات
```

## التشغيل في Replit
- **المنفذ**: 5000 (مطلوب للواجهة الأمامية)
- **الخادم**: 0.0.0.0:5000
- **أمر التشغيل**: `uv run python main.py`

## تحسينات SEO المضافة
- عناوين محسنة للبحث العربي
- meta descriptions باللغة العربية
- كلمات مفتاحية مناسبة
- Open Graph tags
- JSON-LD structured data
- hreflang للمحتوى العربي

## التوزيع
- نوع التوزيع: autoscale (للمواقع البسيطة)
- أمر البناء: غير مطلوب
- أمر التشغيل: `uv run python main.py`

## التاريخ
- **إنشاء المشروع**: 2025-09-19
- **آخر تحديث**: 2025-09-19
- **الحالة**: جاهز للإنتاج