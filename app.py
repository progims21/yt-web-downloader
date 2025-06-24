import streamlit as st
import subprocess
import os
import uuid
import glob
from datetime import datetime
import webbrowser
import re
import time  # Added missing import

# Page settings
st.set_page_config(
    page_title="🎬 نظام التحميل الفني المتقدم",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### نظام التحميل الفني المتقدم\nإصدار 4.1\nالمطور: طالب الأنظمة الطبية\nالدعم: rshqrwsy@gmail.com"
    }
)

# Enhanced colors and animations
st.markdown("""
<style>
:root {
    --primary: #43022e;
    --secondary: #F4d0c9;
    --accent: #aa8b9f;
    --background: #fff5f3;
    --text: #333333;
    --success: #4CAF50;
    --warning: #FFC107;
    --error: #F44336;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px); }
    40%, 80% { transform: translateX(5px); }
}

.stApp {
    background-color: var(--background);
    color: var(--text);
    font-family: 'Arial', sans-serif;
}

.stTextInput>div>div>input {
    border: 2px solid var(--primary);
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    transition: all 0.3s;
    animation: fadeIn 0.6s ease-out;
}

.stTextInput>div>div>input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--secondary);
}

.stButton>button {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-weight: bold;
    font-size: 16px;
    transition: all 0.3s;
    animation: fadeIn 0.8s ease-out;
}

.stButton>button:hover {
    background-color: var(--accent);
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(67, 2, 46, 0.2);
}

.stDownloadButton>button {
    background-color: var(--success);
    color: white;
    border-radius: 12px;
    padding: 14px 28px;
    animation: pulse 2s infinite;
}

.stDownloadButton>button:hover {
    background-color: #45a049;
    animation: none;
    transform: scale(1.05);
}

.css-1aumxhk {
    background-color: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(67, 2, 46, 0.1);
    margin-bottom: 24px;
    border: 1px solid var(--secondary);
    animation: fadeIn 1s ease-out;
}

.header {
    color: var(--primary);
    text-align: center;
    margin-bottom: 30px;
    animation: fadeIn 0.5s ease-out;
}

.social-btn {
    display: inline-block;
    background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
    color: white !important;
    padding: 10px 20px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: bold;
    margin: 10px 5px;
    transition: all 0.3s;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.social-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.fb-btn {
    background: linear-gradient(45deg, #1877f2, #0d5ab9) !important;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    background-color: var(--primary);
    color: white;
    border-radius: 16px;
    animation: fadeIn 1.2s ease-out;
}

.warning-box {
    background-color: var(--warning);
    color: #000;
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    animation: fadeIn 0.5s ease-out;
}

.error-box {
    background-color: var(--error);
    color: white;
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    animation: shake 0.5s ease-in-out;
}

.success-box {
    background-color: var(--success);
    color: white;
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    animation: fadeIn 0.5s ease-out;
}

.progress-bar {
    height: 10px;
    background-color: var(--secondary);
    border-radius: 5px;
    margin: 15px 0;
    overflow: hidden;
}

.progress {
    height: 100%;
    background-color: var(--primary);
    width: 0%;
    transition: width 0.3s ease;
}

.platform-tag {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    margin-left: 10px;
}

.youtube-tag {
    background-color: #FF0000;
    color: white;
}

.instagram-tag {
    background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
    color: white;
}

.facebook-tag {
    background-color: #1877f2;
    color: white;
}

.tiktok-tag {
    background-color: #000000;
    color: white;
}

.twitter-tag {
    background-color: #1DA1F2;
    color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .stButton>button {
        padding: 10px 20px;
        font-size: 14px;
    }
    
    .stTextInput>div>div>input {
        padding: 10px;
        font-size: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# Main interface
st.markdown('<div class="header"><h1>🎬 نظام التحميل الفني المتقدم</h1></div>', unsafe_allow_html=True)

# Social media links section
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <a href="https://www.instagram.com/mc.love.98" class="social-btn" target="_blank">تابعنا @mc.love.98</a>
        <a href="https://www.facebook.com/" class="social-btn fb-btn" target="_blank">فيسبوك</a>
    </div>
    """, unsafe_allow_html=True)

# Main input section
with st.container():
    url = st.text_input("", placeholder="الصق رابط يوتيوب أو إنستجرام أو فيسبوك أو تيك توك أو تويتر هنا", label_visibility="collapsed", key="url_input")

# Download options
with st.expander("⚙️ خيارات التحميل المتقدمة", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        format_option = st.radio("نوع الملف:", ["🎥 فيديو", "🎵 صوت", "📼 قصص/ريلز"])
    with col2:
        if format_option == "🎥 فيديو":
            quality = st.selectbox("جودة الفيديو:", ["أفضل جودة", "4K/2160p", "1080p/FHD", "720p/HD", "480p/SD"])
        elif format_option == "🎵 صوت":
            quality = st.selectbox("جودة الصوت:", ["أفضل جودة (320kbps)", "جودة عالية (256kbps)", "جودة متوسطة (192kbps)"])
        else:
            quality = st.selectbox("جودة القصص:", ["أفضل جودة", "جودة عالية"])
    with col3:
        custom_name = st.text_input("اسم مخصص للملف:", placeholder="اختياري")

# New feature: Download range
with st.expander("🔍 خيارات إضافية (اختياري)"):
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <p>يمكنك تحديد جزء معين من الفيديو للتحميل (بالثواني)</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input("وقت البداية (ثانية):", min_value=0, value=0)
    with col2:
        end_time = st.number_input("وقت النهاية (ثانية):", min_value=0, value=0)
    
    # Add metadata options
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <p>خيارات البيانات الوصفية (للفيديوهات والصوت فقط)</p>
    </div>
    """, unsafe_allow_html=True)
    add_metadata = st.checkbox("إضافة البيانات الوصفية (العنوان، الفنان، إلخ)", value=True)

# Download button
if st.button("🚀 بدء التحميل", use_container_width=True, type="primary"):
    if not url.strip():
        st.markdown('<div class="error-box">⚠️ يرجى إدخال رابط صحيح</div>', unsafe_allow_html=True)
    else:
        with st.spinner("⏳ جاري معالجة طلبك... الرجاء الانتظار"):
            try:
                # Determine platform type
                if "instagram.com" in url:
                    platform = "Instagram"
                    platform_tag = "instagram-tag"
                    if "stories" in url.lower() or "reels" in url.lower() or format_option == "📼 قصص/ريلز":
                        format_option = "📼 قصص/ريلز"
                elif "facebook.com" in url or "fb.watch" in url:
                    platform = "Facebook"
                    platform_tag = "facebook-tag"
                elif "tiktok.com" in url:
                    platform = "TikTok"
                    platform_tag = "tiktok-tag"
                elif "twitter.com" in url or "x.com" in url:
                    platform = "Twitter"
                    platform_tag = "twitter-tag"
                else:
                    platform = "YouTube"
                    platform_tag = "youtube-tag"
                
                # Create downloads folder
                os.makedirs("downloads", exist_ok=True)
                
                # Build filename
                if custom_name:
                    filename = f"{custom_name}.%(ext)s"
                else:
                    filename = f"%(title)s.%(ext)s"
                
                # Build download command
                cmd = []
                
                # Base command
                if platform == "YouTube":
                    cmd.append('yt-dlp')
                    
                    if format_option == "🎥 فيديو":
                        quality_map = {
                            "أفضل جودة": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                            "4K/2160p": "313+251",
                            "1080p/FHD": "137+140",
                            "720p/HD": "22",
                            "480p/SD": "135+140"
                        }
                        cmd.extend(['-f', f'"{quality_map[quality]}"', '--merge-output-format', 'mp4'])
                    elif format_option == "🎵 صوت":
                        quality_map = {
                            "أفضل جودة (320kbps)": "320K",
                            "جودة عالية (256kbps)": "256K",
                            "جودة متوسطة (192kbps)": "192K"
                        }
                        cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', quality_map[quality]])
                else:  # Instagram, Facebook, TikTok, Twitter
                    cmd.append('yt-dlp')
                    
                    if format_option == "📼 قصص/ريلز":
                        cmd.extend(['-f', 'best', '--cookies-from-browser', 'chrome'])
                    else:
                        cmd.extend(['-f', 'best'])
                
                # Add metadata if requested
                if add_metadata and format_option != "📼 قصص/ريلز":
                    cmd.extend(['--add-metadata', '--embed-thumbnail'])
                
                # Add download range if specified
                if start_time > 0 or end_time > 0:
                    if end_time > start_time:
                        cmd.extend(['--download-sections', f'"*{start_time}-{end_time}"'])
                    else:
                        st.markdown('<div class="warning-box">⚠️ وقت النهاية يجب أن يكون أكبر من وقت البداية</div>', unsafe_allow_html=True)
                
                # Add output path and URL
                cmd.extend(['-o', f'"downloads/{filename}"', f'"{url}"'])
                
                # Convert command list to string
                cmd_str = ' '.join(cmd)
                
                # Progress bar (simulated)
                progress_bar = st.empty()
                progress_bar.markdown('<div class="progress-bar"><div class="progress" style="width: 0%"></div></div>', unsafe_allow_html=True)
                
                # Simulate progress
                for percent in range(0, 101, 5):
                    progress_bar.markdown(f'<div class="progress-bar"><div class="progress" style="width: {percent}%"></div></div>', unsafe_allow_html=True)
                    time.sleep(0.1)
                
                # Execute download
                result = subprocess.run(cmd_str, shell=True, check=True, capture_output=True, text=True)
                
                # Find downloaded file
                downloaded_files = glob.glob("downloads/*")
                if downloaded_files:
                    # Find the newest file
                    latest_file = max(downloaded_files, key=os.path.getctime)
                    
                    with open(latest_file, "rb") as f:
                        file_name = os.path.basename(latest_file)
                        file_size = os.path.getsize(latest_file) / (1024 * 1024)  # in MB
                        
                        st.markdown(f"""
                        <div class="success-box">
                            ✅ تم التحميل بنجاح! 
                            <span class="platform-tag {platform_tag}">{platform}</span>
                            <br>حجم الملف: {file_size:.2f} MB
                            <br>نوع الملف: {format_option.split()[1]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.balloons()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "💾 حفظ الملف",
                                data=f,
                                file_name=file_name,
                                use_container_width=True
                            )
                        with col2:
                            st.write(f"**وقت التحميل:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            st.write(f"**الجودة:** {quality}")
                    
                    # Delete temporary file
                    os.remove(latest_file)
                else:
                    st.markdown('<div class="error-box">❌ لم يتم العثور على الملف المحمل</div>', unsafe_allow_html=True)
                
                # Show download details
                with st.expander("📊 تفاصيل التحميل"):
                    st.code(result.stdout)
                    
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr if e.stderr else "حدث خطأ أثناء عملية التحميل"
                st.markdown(f'<div class="error-box">❌ خطأ في التحميل: {error_msg}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ حدث خطأ غير متوقع: {str(e)}</div>', unsafe_allow_html=True)

# How-to guide section
with st.expander("❓ دليل الاستخدام", expanded=False):
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <h3>كيفية استخدام النظام:</h3>
    <ol>
        <li>قم بنسخ رابط الفيديو أو المنشور من YouTube أو Instagram أو Facebook أو TikTok أو Twitter</li>
        <li>الصق الرابط في الحقل المخصص بالأعلى</li>
        <li>اختر نوع الملف الذي تريد تحميله (فيديو، صوت، أو قصص/ريلز)</li>
        <li>حدد الجودة المطلوبة</li>
        <li>يمكنك إضافة اسم مخصص للملف إذا رغبت (اختياري)</li>
        <li>اضغط على زر "بدء التحميل"</li>
        <li>انتظر حتى يكتمل التحميل ثم اضغط على زر "حفظ الملف"</li>
    </ol>
    
    <h3>ملاحظات مهمة:</h3>
    <ul>
        <li>لتحميل القصص أو الريلز من Instagram، تأكد من أن الحساب عام</li>
        <li>لتحميل مقاطع طويلة من YouTube، يمكنك تحديد نطاق زمني من الخيارات الإضافية</li>
        <li>لأفضل النتائج، استخدم اتصال إنترنت مستقر</li>
        <li>لتحميل منصات مثل Facebook وInstagram، قد تحتاج إلى تسجيل الدخول في المتصفح أولاً</li>
    </ul>
    
    <h3>الميزات الجديدة:</h3>
    <ul>
        <li>دعم منصات إضافية: TikTok وTwitter</li>
        <li>إضافة البيانات الوصفية تلقائياً للفيديوهات والمقاطع الصوتية</li>
        <li>واجهة مستخدم أكثر تفاعلية وسريعة</li>
        <li>تحسينات في أداء التحميل</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Page footer
st.markdown("""
<div class="footer">
    <p><strong>نظام التحميل الفني المتقدم © 2025</strong></p>
    <p>تم التطوير بواسطة طالب الأنظمة الطبية</p>
    <p>للتواصل والدعم: <a href="mailto:rshqrwsy@gmail.com" style="color: var(--secondary);">rshqrwsy@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)

# Social media links in sidebar
with st.sidebar:
    st.markdown("## 📱 تابعنا على")
    if st.button("إنستجرام @mc.love.98", key="insta"):
        webbrowser.open_new_tab("https://www.instagram.com/mc.love.98")
    if st.button("فيسبوك", key="fb"):
        webbrowser.open_new_tab("https://www.facebook.com/")
    
    st.markdown("---")
    st.markdown("### 🔥 مميزات جديدة")
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <ul>
        <li>دعم منصات جديدة: TikTok وTwitter</li>
        <li>إضافة البيانات الوصفية تلقائياً</li>
        <li>تحسينات في أداء التحميل</li>
        <li>واجهة مستخدم محسنة</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ حالة النظام")
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <p><strong>الإصدار:</strong> 4.1</p>
    <p><strong>الحالة:</strong> نشط</p>
    <p><strong>آخر تحديث:</strong> {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎨 ألوان التصميم")
    st.markdown("""
    <div style="background-color: #43022e; color: white; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
        اللون الأساسي: #43022e
    </div>
    <div style="background-color: #F4d0c9; padding: 10px; border-radius: 8px;">
        اللون الثانوي: #F4d0c9
    </div>
    """, unsafe_allow_html=True)