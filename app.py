import streamlit as st
import subprocess
import os
import uuid
import glob
from datetime import datetime
import webbrowser

# إعدادات الصفحة
st.set_page_config(
    page_title="🎬 نظام التحميل الفني",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ألوان فنية (#F4d0c9 و #43022e) مع موشن قوي
st.markdown("""
<style>
:root {
    --primary: #43022e;
    --secondary: #F4d0c9;
    --accent: #aa8b9f;
    --background: #fff5f3;
    --text: #333333;
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
    background-color: var(--primary);
    color: white;
    border-radius: 12px;
    padding: 14px 28px;
    animation: pulse 2s infinite;
}

.stDownloadButton>button:hover {
    background-color: var(--accent);
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
</style>
""", unsafe_allow_html=True)

# الواجهة الرئيسية
st.markdown('<div class="header"><h1>🎬 نظام التحميل الفني المتكامل</h1></div>', unsafe_allow_html=True)

# قسم روابط التواصل الاجتماعي
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <a href="https://www.instagram.com/" class="social-btn" target="_blank">إنستجرام</a>
        <a href="https://www.facebook.com/" class="social-btn fb-btn" target="_blank">فيسبوك</a>
    </div>
    """, unsafe_allow_html=True)

# قسم الإدخال الرئيسي
with st.container():
    url = st.text_input("", placeholder="الصق رابط يوتيوب أو إنستجرام أو فيسبوك هنا", label_visibility="collapsed")

# خيارات التحميل
with st.expander("⚙️ خيارات التحميل", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        format_option = st.radio("نوع الملف:", ["🎥 فيديو", "🎵 صوت"], horizontal=True)
    with col2:
        quality = st.selectbox("الجودة:", ["أفضل جودة", "عالية الدقة", "جودة متوسطة"])

# زر التحميل
if st.button("🚀 بدء التحميل", use_container_width=True, type="primary"):
    if not url.strip():
        st.warning("⚠️ يرجى إدخال رابط صحيح")
    else:
        with st.spinner("⏳ جاري التحميل... الرجاء الانتظار"):
            try:
                uid = str(uuid.uuid4())
                os.makedirs("downloads", exist_ok=True)
                
                # تحديد نوع الرابط
                if "instagram.com" in url:
                    platform = "Instagram"
                    cmd = f'yt-dlp -f best -o "downloads/{uid}.%(ext)s" "{url}"'
                elif "facebook.com" in url:
                    platform = "Facebook"
                    cmd = f'yt-dlp -f best -o "downloads/{uid}.%(ext)s" "{url}"'
                else:
                    platform = "YouTube"
                    if format_option == "🎥 فيديو":
                        quality_map = {
                            "أفضل جودة": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                            "عالية الدقة": "22",
                            "جودة متوسطة": "18"
                        }
                        cmd = f'yt-dlp -f "{quality_map[quality]}" --merge-output-format mp4 -o "downloads/{uid}.%(ext)s" "{url}"'
                    else:
                        quality_map = {
                            "أفضل جودة": "bestaudio",
                            "عالية الدقة": "--audio-quality 320K",
                            "جودة متوسطة": "--audio-quality 192K"
                        }
                        cmd = f'yt-dlp -x --audio-format mp3 {quality_map[quality]} -o "downloads/{uid}.%(ext)s" "{url}"'
                
                subprocess.run(cmd, shell=True, check=True)
                
                # البحث عن الملف المحمل
                downloaded_files = glob.glob(f"downloads/{uid}.*")
                if downloaded_files:
                    file_path = downloaded_files[0]
                    with open(file_path, "rb") as f:
                        st.success(f"✅ تم تحميل {platform} بنجاح!")
                        st.balloons()
                        st.download_button(
                            "💾 حفظ الملف",
                            data=f,
                            file_name=os.path.basename(file_path),
                            use_container_width=True
                        )
                    os.remove(file_path)
                else:
                    st.error("❌ لم يتم العثور على الملف المحمل")
                    
            except subprocess.CalledProcessError as e:
                st.error(f"❌ خطأ في التحميل: {e.stderr}")
            except Exception as e:
                st.error(f"❌ حدث خطأ غير متوقع: {e}")

# تذييل الصفحة
st.markdown("""
<div class="footer">
    <p><strong>نظام التحميل الفني المتكامل © 2025</strong></p>
    <p>تم التطوير بواسطة طالب الأنظمة الطبية</p>
    <p>للتواصل والدعم: <a href="mailto:rshqrwsy@gmail.com" style="color: var(--secondary);">rshqrwsy@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)

# روابط التواصل الاجتماعي في الشريط الجانبي
with st.sidebar:
    st.markdown("## 📱 تابعنا على")
    if st.button("إنستجرام", key="insta"):
        webbrowser.open_new_tab("https://www.instagram.com/")
    if st.button("فيسبوك", key="fb"):
        webbrowser.open_new_tab("https://www.facebook.com/")
    
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