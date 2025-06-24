import streamlit as st
import subprocess
import os
import uuid
import re
import shutil
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="المبرمجون الأحرار – YouTube Downloader", 
    layout="centered", 
    page_icon="📥"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff6b6b;
        margin-bottom: 30px;
    }
    .download-info {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📥 المبرمجون الأحرار – تحميل من YouTube</h1>', unsafe_allow_html=True)

# Create downloads directory
downloads_dir = Path("downloads")
downloads_dir.mkdir(exist_ok=True)

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/',
        r'(https?://)?(www\.)?youtu\.be/',
    ]
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def get_video_info(url):
    """Get video information using yt-dlp"""
    try:
        cmd = f'yt-dlp --print title --print duration --print uploader "{url}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return {
                'title': lines[0] if len(lines) > 0 else 'Unknown',
                'duration': lines[1] if len(lines) > 1 else 'Unknown',
                'uploader': lines[2] if len(lines) > 2 else 'Unknown'
            }
    except Exception:
        pass
    return None

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    try:
        current_time = time.time()
        for file_path in downloads_dir.glob("*"):
            if file_path.is_file() and (current_time - file_path.stat().st_mtime) > 3600:
                file_path.unlink()
    except Exception:
        pass

def download_video(url, format_option, quality, uid):
    """Download video with improved error handling"""
    template = str(downloads_dir / f"{uid}.%(ext)s")
    
    if format_option == "📺 فيديو":
        if quality == "best":
            format_selector = "best[height<=1080]"
        else:
            height = quality.replace('p', '')
            format_selector = f"best[height<={height}]"
        cmd = f'yt-dlp -f "{format_selector}" -o "{template}" "{url}"'
    else:
        cmd = f'yt-dlp -f "bestaudio" -x --audio-format mp3 --audio-quality 0 -o "{template}" "{url}"'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            # Find the downloaded file
            for file_path in downloads_dir.glob(f"{uid}.*"):
                return file_path
        else:
            raise Exception(result.stderr or "Download failed")
    except subprocess.TimeoutExpired:
        raise Exception("التحميل استغرق وقتاً أطول من المتوقع")
    
    return None

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "أدخل رابط الفيديو:",
        placeholder="https://www.youtube.com/watch?v=xxxx أو https://youtu.be/xxxx",
        help="يدعم روابط YouTube و YouTube Shorts"
    )

with col2:
    if st.button("🔍 معاينة"):
        if url.strip() and validate_youtube_url(url):
            with st.spinner("جاري جلب معلومات الفيديو..."):
                video_info = get_video_info(url)
                if video_info:
                    st.session_state.video_info = video_info
                else:
                    st.error("لا يمكن جلب معلومات الفيديو")
        elif url.strip():
            st.error("رابط غير صالح. الرجاء إدخال رابط YouTube صحيح")

# Display video info if available
if hasattr(st.session_state, 'video_info') and st.session_state.video_info:
    info = st.session_state.video_info
    st.markdown(f"""
    <div class="download-info">
        <strong>📹 العنوان:</strong> {info['title']}<br>
        <strong>⏱️ المدة:</strong> {info['duration']}<br>
        <strong>👤 القناة:</strong> {info['uploader']}
    </div>
    """, unsafe_allow_html=True)

# Download options
col1, col2 = st.columns(2)

with col1:
    format_option = st.radio(
        "اختر الصيغة:",
        ["📺 فيديو", "🎵 صوت (MP3)"],
        help="اختر فيديو للحصول على الصوت والصورة، أو صوت للحصول على MP3 فقط"
    )

with col2:
    if format_option == "📺 فيديو":
        quality = st.selectbox(
            "الجودة:",
            ["best", "1080p", "720p", "480p", "360p"],
            help="best = أفضل جودة متاحة"
        )
    else:
        quality = st.selectbox(
            "جودة الصوت:",
            ["أفضل جودة", "جودة عالية", "جودة متوسطة"],
            help="أفضل جودة = 320kbps تقريباً"
        )

# Advanced options
with st.expander("⚙️ خيارات متقدمة"):
    col1, col2 = st.columns(2)
    with col1:
        custom_name = st.text_input("اسم مخصص للملف (اختياري):")
    with col2:
        start_time = st.text_input("وقت البداية (mm:ss أو hh:mm:ss):", placeholder="مثال: 1:30")
        end_time = st.text_input("وقت النهاية (mm:ss أو hh:mm:ss):", placeholder="مثال: 5:45")

# Download button
if st.button("🚀 ابدأ التحميل", type="primary", use_container_width=True):
    if not url.strip():
        st.warning("⚠️ الرجاء إدخال رابط صحيح")
    elif not validate_youtube_url(url):
        st.error("❌ الرابط المُدخل ليس رابط YouTube صحيح")
    else:
        # Clean up old files
        cleanup_old_files()
        
        uid = str(uuid.uuid4())[:8]  # Shorter UID
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("⏳ بدء التحميل...")
            progress_bar.progress(25)
            
            downloaded_file = download_video(url, format_option, quality, uid)
            progress_bar.progress(75)
            
            if downloaded_file and downloaded_file.exists():
                progress_bar.progress(100)
                status_text.empty()
                
                # Custom filename handling
                final_filename = downloaded_file.name
                if custom_name:
                    extension = downloaded_file.suffix
                    safe_name = re.sub(r'[^\w\s-]', '', custom_name)
                    final_filename = f"{safe_name}{extension}"
                
                # Read file for download
                with open(downloaded_file, "rb") as f:
                    file_data = f.read()
                
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ تم التحميل بنجاح!</strong><br>
                    📁 اسم الملف: {final_filename}<br>
                    📊 حجم الملف: {len(file_data) / (1024*1024):.2f} MB
                </div>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="📂 تحميل الملف",
                    data=file_data,
                    file_name=final_filename,
                    mime="application/octet-stream",
                    use_container_width=True
                )
                
                # Clean up the downloaded file
                try:
                    downloaded_file.unlink()
                except Exception:
                    pass
            else:
                st.error("❌ فشل في التحميل. تأكد من صحة الرابط وإعادة المحاولة")
                
        except Exception as err:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="error-box">
                <strong>❌ حدث خطأ أثناء التحميل:</strong><br>
                {str(err)}
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 30px;'>
    <p>🔧 تم تطويره بواسطة المبرمجون الأحرار</p>
    <p>⚠️ يرجى احترام حقوق الطبع والنشر عند استخدام هذه الأداة</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.header("📖 تعليمات الاستخدام")
    st.markdown("""
    **كيفية الاستخدام:**
    1. انسخ رابط الفيديو من YouTube
    2. الصقه في الحقل المخصص
    3. اضغط "معاينة" لرؤية معلومات الفيديو
    4. اختر الصيغة والجودة المطلوبة
    5. اضغط "ابدأ التحميل"
    
    **أنواع الروابط المدعومة:**
    - `youtube.com/watch?v=...`
    - `youtu.be/...`
    - YouTube Shorts
    - قوائم التشغيل (سيتم تحميل الفيديو الأول)
    
    **نصائح:**
    - استخدم "best" للحصول على أفضل جودة
    - ملفات MP3 تكون أصغر حجماً
    - يمكنك تخصيص اسم الملف
    """)
    
    st.header("🆘 استكشاف الأخطاء")
    st.markdown("""
    **إذا واجهت مشاكل:**
    - تأكد من صحة الرابط
    - جرب جودة أقل
    - تأكد من اتصال الإنترنت
    - بعض الفيديوهات قد تكون محمية
    """)
