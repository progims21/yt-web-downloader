import streamlit as st
import subprocess
import os
import uuid
import glob
from datetime import datetime
import webbrowser
import time

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام التحميل الفني المتقدم",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم بسيط
st.markdown("""
<style>
.stApp {
    background-color: #f5f5f5;
    font-family: Arial, sans-serif;
}
.stButton>button {
    background-color: #43022e;
    color: white;
    border-radius: 8px;
    padding: 10px 24px;
}
.stDownloadButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

# الواجهة الرئيسية
st.title("🎬 نظام التحميل الفني المتقدم")

# قسم الإدخال
url = st.text_input("", placeholder="الصق رابط يوتيوب أو إنستجرام أو فيسبوك هنا", label_visibility="collapsed")

# خيارات التحميل
with st.expander("⚙️ خيارات التحميل", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        format_option = st.radio("نوع الملف:", ["فيديو", "صوت"])
    with col2:
        if format_option == "فيديو":
            quality = st.selectbox("جودة الفيديو:", ["أفضل جودة", "1080p", "720p", "480p"])
        else:
            quality = st.selectbox("جودة الصوت:", ["أفضل جودة", "جودة عالية", "جودة متوسطة"])

# زر التحميل
if st.button("بدء التحميل", use_container_width=True):
    if not url.strip():
        st.error("⚠️ يرجى إدخال رابط صحيح")
    else:
        with st.spinner("جاري التحميل... الرجاء الانتظار"):
            try:
                # إنشاء مجلد التحميلات
                os.makedirs("downloads", exist_ok=True)
                
                # بناء أمر التحميل
                cmd = ["yt-dlp"]
                
                if format_option == "فيديو":
                    cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"])
                else:
                    cmd.extend(["-x", "--audio-format", "mp3"])
                
                cmd.extend(["-o", "downloads/%(title)s.%(ext)s", url])
                
                # تنفيذ التحميل
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # البحث عن الملف المحمل
                downloaded_files = glob.glob("downloads/*")
                if downloaded_files:
                    latest_file = max(downloaded_files, key=os.path.getctime)
                    
                    with open(latest_file, "rb") as f:
                        file_name = os.path.basename(latest_file)
                        st.success("تم التحميل بنجاح!")
                        st.download_button(
                            "حفظ الملف",
                            data=f,
                            file_name=file_name,
                            use_container_width=True
                        )
                    
                    # حذف الملف المؤقت
                    os.remove(latest_file)
                else:
                    st.error("❌ لم يتم العثور على الملف المحمل")
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# تذييل الصفحة
st.markdown("---")
st.markdown("تم التطوير بواسطة طالب الأنظمة الطبية | للتواصل: rshqrwsy@gmail.com")