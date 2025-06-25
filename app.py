import streamlit as st
import subprocess
import os
import glob
from datetime import datetime
import time
import re

def safe_escape_url(url):
    """Safe URL escaping function compatible with all Python versions"""
    try:
        # Try using shlex.quote (Python 3.3+)
        import shlex
        if hasattr(shlex, 'quote'):
            return shlex.quote(url)
    except:
        pass
    
    try:
        # Fallback to pipes.quote (deprecated but available)
        import pipes
        return pipes.quote(url)
    except:
        pass
    
    # Manual escaping as last resort
    import re
    # Escape special shell characters
    return re.sub(r'([;&|`$(){}[\]<>"\'\s])', r'\\\1', url)

# إعدادات الصفحة
st.set_page_config(
    page_title="🎬 نظام التحميل الذكي",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم متحرك مع مؤثرات باستخدام الألوان المحددة
st.markdown(f"""
<style>
:root {{
    --primary-color: #DE7A5F;
    --secondary-color: #F3F2DE;
    --text-color: #333333;
    --light-text: #FFFFFF;
}}

@keyframes fadeIn {{
    from {{opacity: 0; transform: translateY(10px);}}
    to {{opacity: 1; transform: translateY(0);}}
}}

@keyframes pulse {{
    0% {{transform: scale(1);}}
    50% {{transform: scale(1.02);}}
    100% {{transform: scale(1);}}
}}

.stApp {{
    background-color: var(--secondary-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    animation: fadeIn 0.5s ease-out;
    color: var(--text-color);
    direction: rtl;
}}

.stButton>button {{
    background-color: var(--primary-color);
    color: var(--light-text);
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: bold;
    transition: all 0.3s;
    animation: fadeIn 0.8s ease-out;
}}

.stButton>button:hover {{
    background-color: #C56950;
    transform: scale(1.03);
    box-shadow: 0 4px 12px rgba(222, 122, 95, 0.3);
}}

.stDownloadButton>button {{
    background-color: var(--primary-color);
    color: var(--light-text);
    border-radius: 12px;
    padding: 12px 28px;
    animation: pulse 2s infinite;
}}

.stDownloadButton>button:hover {{
    animation: none;
    transform: scale(1.03);
    background-color: #C56950;
}}

.stProgress>div>div>div>div {{
    background-color: var(--primary-color) !important;
}}

.css-1aumxhk {{
    background-color: var(--secondary-color);
    border: 1px solid var(--primary-color);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: all 0.3s;
}}

.css-1aumxhk:hover {{
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    border-color: #C56950;
}}

.header {{
    color: var(--primary-color);
    text-align: center;
    margin-bottom: 30px;
    animation: fadeIn 0.6s ease-out;
    padding: 15px;
    background-color: rgba(222, 122, 95, 0.1);
    border-radius: 15px;
}}

.success-animation {{
    animation: fadeIn 0.5s, pulse 1s 2;
}}

.stTextInput>div>div>input {{
    border: 2px solid var(--primary-color) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    direction: rtl;
}}

.stSelectbox>div>div>select {{
    border: 2px solid var(--primary-color) !important;
    border-radius: 12px !important;
}}

.stRadio>div {{
    flex-direction: row !important;
    gap: 20px;
    direction: rtl;
}}

.stRadio>div>label {{
    margin-right: 15px;
}}

.stExpander {{
    border: 1px solid var(--primary-color) !important;
    border-radius: 12px !important;
}}

.stExpander:hover {{
    border-color: #C56950 !important;
}}

.custom-container {{
    border: 1px solid var(--primary-color);
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    background-color: rgba(222, 122, 95, 0.05);
}}

footer {{
    background-color: var(--primary-color) !important;
    color: var(--light-text) !important;
    padding: 15px !important;
    border-radius: 10px !important;
    text-align: center;
}}

/* RTL support */
.stApp * {{
    text-align: right;
}}

.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# الواجهة الرئيسية
st.markdown('<div class="header"><h1>🎬 نظام التحميل الذكي</h1></div>', unsafe_allow_html=True)

# كشف المنصة
def validate_url(url):
    """Validate and sanitize URL input to prevent command injection"""
    if not url or not isinstance(url, str):
        return False, "Invalid URL"
    
    # Remove any whitespace
    url = url.strip()
    
    # Check for basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "URL format is invalid"
    
    # Check for dangerous characters that could be used for command injection
    dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '{', '}', '<', '>', '"', "'"]
    if any(char in url for char in dangerous_chars):
        return False, "URL contains potentially dangerous characters"
    
    # Additional length check
    if len(url) > 2048:
        return False, "URL is too long"
    
    return True, url

def detect_platform(url):
    """Detect the platform from the URL"""
    if not url:
        return "Unknown"
    
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"
    elif "instagram.com" in url:
        if "/reel/" in url or "/reels/" in url:
            return "Instagram Reels"
        elif "/stories/" in url:
            return "Instagram Stories"
        elif "/p/" in url:
            return "Instagram Post"
        return "Instagram"
    elif "facebook.com" in url or "fb.watch" in url:
        return "Facebook"
    elif "tiktok.com" in url:
        return "TikTok"
    elif "twitter.com" in url or "x.com" in url:
        return "Twitter"
    return "Unknown"

def ensure_downloads_directory():
    """Ensure downloads directory exists"""
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

def clean_old_files():
    """Clean old downloaded files"""
    try:
        downloads_dir = "downloads"
        if os.path.exists(downloads_dir):
            for file_path in glob.glob(os.path.join(downloads_dir, "*")):
                if os.path.isfile(file_path):
                    # Remove files older than 1 hour
                    if time.time() - os.path.getctime(file_path) > 3600:
                        os.remove(file_path)
    except Exception as e:
        st.warning(f"تنبيه: فشل في تنظيف الملفات القديمة: {str(e)}")

# Initialize session state
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0

# Clean old files on startup
clean_old_files()

# قسم الإدخال
url = st.text_input(
    "رابط الفيديو:", 
    placeholder="الصق رابط الفيديو هنا (يدعم يوتيوب، إنستجرام، فيسبوك، تيك توك، تويتر)", 
    label_visibility="collapsed"
)

if url:
    is_valid, validated_url = validate_url(url)
    if not is_valid:
        st.error(f"❌ خطأ في الرابط: {validated_url}")
        url = None  # Reset URL to prevent further processing
    else:
        url = validated_url  # Use the validated URL
        platform = detect_platform(url)
        st.info(f"🔍 تم التعرف على المنصة: {platform}")

# خيارات متقدمة
with st.expander("⚙️ خيارات التحميل المتقدمة", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        format_option = st.radio("نوع الملف:", ["فيديو", "صوت", "قصص/ريلز"], index=0)
    
    with col2:
        if format_option == "فيديو":
            quality = st.selectbox("الجودة:", ["أفضل جودة", "1080p", "720p", "480p"])
        elif format_option == "صوت":
            quality = st.selectbox("الجودة:", ["أفضل جودة", "192kbps", "128kbps"])
        else:
            quality = st.selectbox("الجودة:", ["أفضل جودة", "عالية"])
    
    with col3:
        custom_name = st.text_input("اسم الملف (اختياري):", placeholder="اسم الملف المخصص")
        
    # خيارات إضافية
    st.markdown('<div class="custom-container"><h4>خيارات إضافية</h4></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input("وقت البداية (ثانية):", min_value=0, value=0)
    with col2:
        end_time = st.number_input("وقت النهاية (ثانية):", min_value=0, value=0)
    
    add_metadata = st.checkbox("إضافة معلومات الفيديو", value=True)
    embed_thumbnail = st.checkbox("إضافة صورة مصغرة (للملفات الصوتية)", value=True)

# زر التحميل
if st.button("🚀 بدء التحميل", use_container_width=True, type="primary"):
    if not url.strip():
        st.error("⚠️ يرجى إدخال رابط صحيح")
    else:
        # Ensure downloads directory exists
        ensure_downloads_directory()
        
        with st.spinner("جاري معالجة طلبك... الرجاء الانتظار"):
            try:
                # شريط التقدم المتحرك
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # محاكاة التقدم
                status_text.text("🔍 جاري فحص الرابط...")
                for percent in range(0, 21, 5):
                    time.sleep(0.1)
                    progress_bar.progress(percent)
                
                status_text.text("⚙️ جاري إعداد خيارات التحميل...")
                for percent in range(21, 41, 5):
                    time.sleep(0.1)
                    progress_bar.progress(percent)
                
                # بناء أمر التحميل
                cmd = ["yt-dlp"]
                
                # إعداد خيارات الجودة
                if format_option == "فيديو":
                    if quality == "1080p":
                        cmd.extend(["-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"])
                    elif quality == "720p":
                        cmd.extend(["-f", "bestvideo[height<=720]+bestaudio/best[height<=720]"])
                    elif quality == "480p":
                        cmd.extend(["-f", "bestvideo[height<=480]+bestaudio/best[height<=480]"])
                    else:
                        cmd.extend(["-f", "bestvideo+bestaudio/best"])
                elif format_option == "صوت":
                    cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
                    if quality == "192kbps":
                        cmd.extend(["--postprocessor-args", "-ab 192k"])
                    elif quality == "128kbps":
                        cmd.extend(["--postprocessor-args", "-ab 128k"])
                    else:
                        cmd.extend(["--postprocessor-args", "-ab 320k"])
                
                # خيارات إضافية
                if add_metadata:
                    cmd.append("--add-metadata")
                if embed_thumbnail and format_option == "صوت":
                    cmd.append("--embed-thumbnail")
                if start_time > 0 or end_time > 0:
                    if end_time > start_time:
                        cmd.extend(["--download-sections", f"*{start_time}-{end_time}"])
                
                # اسم الملف المخصص
                if custom_name:
                    safe_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    cmd.extend(["-o", f"downloads/{safe_name}.%(ext)s"])
                else:
                    cmd.extend(["-o", "downloads/%(title)s.%(ext)s"])
                
                # Add the URL directly since it's already validated
                cmd.append(url)
                
                status_text.text("⬇️ جاري التحميل...")
                for percent in range(41, 91, 10):
                    time.sleep(0.2)
                    progress_bar.progress(percent)
                
                # تنفيذ التحميل
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                status_text.text("📁 جاري معالجة الملف...")
                for percent in range(91, 101, 3):
                    time.sleep(0.1)
                    progress_bar.progress(percent)
                
                # العثور على الملف المحمل
                downloaded_files = glob.glob("downloads/*")
                downloaded_files = [f for f in downloaded_files if os.path.isfile(f)]
                
                if downloaded_files:
                    latest_file = max(downloaded_files, key=os.path.getctime)
                    file_size = os.path.getsize(latest_file) / (1024 * 1024)  # بالميغابايت
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    with open(latest_file, "rb") as f:
                        file_data = f.read()
                        
                    st.markdown(f'<div class="success-animation">', unsafe_allow_html=True)
                    st.success(f"✅ تم التحميل بنجاح! حجم الملف: {file_size:.2f} MB")
                    st.balloons()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "💾 حفظ الملف",
                            data=file_data,
                            file_name=os.path.basename(latest_file),
                            use_container_width=True
                        )
                    with col2:
                        st.write(f"**نوع الملف:** {format_option}")
                        st.write(f"**الجودة:** {quality}")
                        st.write(f"**وقت التحميل:** {datetime.now().strftime('%H:%M:%S')}")
                        if custom_name:
                            st.write(f"**الاسم المخصص:** {custom_name}")
                    
                    # تنظيف الملف المؤقت
                    try:
                        os.remove(latest_file)
                    except Exception as e:
                        st.warning(f"تنبيه: فشل في حذف الملف المؤقت: {str(e)}")
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ فشل في التحميل، يرجى التحقق من الرابط وإعادة المحاولة")
                    if result.stderr:
                        st.error(f"تفاصيل الخطأ: {result.stderr}")
                
            except subprocess.TimeoutExpired:
                st.error("❌ انتهت مهلة التحميل. يرجى المحاولة مرة أخرى مع فيديو أصغر حجماً")
            except subprocess.CalledProcessError as e:
                st.error(f"❌ خطأ في التحميل: {e.stderr if e.stderr else 'خطأ غير معروف'}")
            except Exception as e:
                st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")

# قسم المساعدة
with st.expander("❓ مساعدة", expanded=False):
    st.markdown("""
    **كيفية الاستخدام:**
    1. الصق رابط الفيديو في الحقل المخصص
    2. اختر نوع الملف وجودته
    3. اضغط على زر "بدء التحميل"
    4. انتظر حتى يكتمل التحميل
    5. اضغط على زر "حفظ الملف" لتنزيله
    
    **المنصات المدعومة:**
    - يوتيوب (YouTube)
    - إنستجرام (Instagram) - منشورات، ريلز، قصص
    - فيسبوك (Facebook)
    - تيك توك (TikTok)
    - تويتر/إكس (Twitter/X)
    
    **نصائح مهمة:**
    - تأكد من أن الرابط صحيح وقابل للوصول
    - بعض المحتوى قد يكون محمي بحقوق الطبع والنشر
    - أوقات التحميل تعتمد على حجم الفيديو وسرعة الإنترنت
    - يتم حذف الملفات تلقائياً بعد التحميل لحماية الخصوصية
    
    **للاستفسارات والدعم:** rshqrwsy@gmail.com
    """)

# معلومات النظام
with st.expander("ℹ️ معلومات النظام", expanded=False):
    st.markdown("""
    **متطلبات النظام:**
    - يتطلب تثبيت yt-dlp
    - يدعم جميع المتصفحات الحديثة
    - يعمل على جميع أنظمة التشغيل
    
    **الإصدار الحالي:** 2.0
    
    **آخر تحديث:** يونيو 2025
    
    **الميزات الجديدة:**
    - دعم محسن للمنصات العربية
    - واجهة مستخدم محسنة
    - تحميل أسرع وأكثر استقراراً
    - دعم أفضل للجودة العالية
    """)

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #DE7A5F; color: white; border-radius: 10px; margin-top: 30px;">
    <h3>🎬 نظام التحميل الذكي - الإصدار 2.0</h3>
    <p>تم التطوير بواسطة طالب الأنظمة الطبية</p>
    <p>📧 للدعم والاستفسارات: rshqrwsy@gmail.com</p>
    <p>⚡ مدعوم بتقنية yt-dlp و Streamlit</p>
</div>
""", unsafe_allow_html=True)
