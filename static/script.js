// Global variables
let currentVideoData = null;

// Utility functions
function showElement(id) {
    document.getElementById(id).style.display = 'block';
}

function hideElement(id) {
    document.getElementById(id).style.display = 'none';
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    showElement('error-section');
    hideElement('loading');
    hideElement('download-section');
}

function clearError() {
    hideElement('error-section');
}

// Main functions
async function fetchInfo() {
    const url = document.getElementById("url").value.trim();
    
    // Validate URL input
    if (!url) {
        showError("ادخل رابط فيديو صحيح يا شيطان 👿");
        return;
    }

    // Validate YouTube URL
    if (!isValidYouTubeUrl(url)) {
        showError("الرابط يجب أن يكون من YouTube فقط!");
        return;
    }

    // Show loading state
    clearError();
    showElement('loading');
    hideElement('download-section');

    try {
        const response = await fetch(`/info?url=${encodeURIComponent(url)}`);
        const data = await response.json();

        hideElement('loading');

        if (data.error) {
            showError(data.error);
            return;
        }

        // Store video data
        currentVideoData = data;

        // Update UI with video information
        updateVideoInfo(data);
        showElement('download-section');

    } catch (error) {
        hideElement('loading');
        showError("حدث خطأ في الاتصال بالخادم. جرب مرة أخرى.");
        console.error('Error fetching video info:', error);
    }
}

function updateVideoInfo(data) {
    // Update video title and thumbnail
    document.getElementById("video-title").textContent = data.title || "عنوان غير متوفر";
    
    const thumbnailImg = document.getElementById("thumb");
    if (data.thumbnail) {
        thumbnailImg.src = data.thumbnail;
        thumbnailImg.style.display = 'block';
    } else {
        thumbnailImg.style.display = 'none';
    }

    // Populate quality options
    const qualitySelect = document.getElementById("quality");
    qualitySelect.innerHTML = '<option value="">اختر الجودة...</option>';

    if (data.formats && data.formats.length > 0) {
        // Sort formats by quality (resolution)
        const sortedFormats = data.formats.sort((a, b) => {
            const heightA = parseInt(a.resolution) || 0;
            const heightB = parseInt(b.resolution) || 0;
            return heightB - heightA; // Descending order
        });

        sortedFormats.forEach(format => {
            const option = document.createElement("option");
            option.value = format.format_id;
            
            const fileSize = format.filesize > 0 ? `${format.filesize} MB` : 'حجم غير معروف';
            option.textContent = `${format.resolution} (${format.ext.toUpperCase()}) - ${fileSize}`;
            
            qualitySelect.appendChild(option);
        });
    } else {
        const option = document.createElement("option");
        option.textContent = "لا توجد جودات متاحة";
        option.disabled = true;
        qualitySelect.appendChild(option);
    }
}

async function downloadVideo() {
    const url = document.getElementById("url").value.trim();
    const quality = document.getElementById("quality").value;

    if (!quality) {
        showError("اختر جودة التحميل أولاً!");
        return;
    }

    // Show download status
    showElement('download-status');
    
    try {
        // Create download link
        const downloadUrl = `/download?url=${encodeURIComponent(url)}&quality=${encodeURIComponent(quality)}`;
        
        // Open download in new tab
        const downloadWindow = window.open(downloadUrl, '_blank');
        
        // Hide download status after a short delay
        setTimeout(() => {
            hideElement('download-status');
        }, 3000);

        // Check if download window was blocked
        if (!downloadWindow) {
            showError("تم حجب النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة وإعادة المحاولة.");
        }

    } catch (error) {
        hideElement('download-status');
        showError("حدث خطأ أثناء بدء التحميل. جرب مرة أخرى.");
        console.error('Download error:', error);
    }
}

async function cleanupFiles() {
    if (!confirm("هل أنت متأكد من حذف جميع الملفات المؤقتة؟")) {
        return;
    }

    try {
        const response = await fetch('/cleanup');
        const data = await response.json();
        
        if (data.error) {
            alert(`خطأ في التنظيف: ${data.error}`);
        } else {
            alert(`تم حذف ${data.deleted} ملف بنجاح`);
        }
    } catch (error) {
        alert("حدث خطأ أثناء تنظيف الملفات");
        console.error('Cleanup error:', error);
    }
}

// Utility function to validate YouTube URLs
function isValidYouTubeUrl(url) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return youtubeRegex.test(url);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add enter key support for URL input
    document.getElementById('url').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            fetchInfo();
        }
    });

    // Add change event for quality selection
    document.getElementById('quality').addEventListener('change', function() {
        clearError();
    });
});

// Add some visual feedback for button clicks
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'BUTTON') {
        e.target.style.transform = 'scale(0.98)';
        setTimeout(() => {
            e.target.style.transform = 'scale(1)';
        }, 100);
    }
});
