import streamlit as st
import subprocess
import os
import uuid
import glob

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام التحميل الطبي",
    page_icon="⬇️",
    layout="centered"
)

# ألوان فخمة بنفسجية ملكية
st.markdown("""
<style>
:root {
    --primary: #6a0dad;
    --secondary: #9c27b0;
    --accent: #e1bee7;
    --background: #f3e5f5;
}

.stApp {
    background-color: var(--background);
}

.stTextInput>div>div>input {
    border: 2px solid var(--primary);
    border-radius: 8px;
    padding: 10px;
}

.stButton>button {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    transition: all 0.3s;
}

.stButton>button:hover {
    background-color: var(--secondary);
    transform: scale(1.02);
}

.stDownloadButton>button {
    background-color: var(--secondary);
    color: white;
}

.css-1aumxhk {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(106, 13, 173, 0.1);
}

.header {
    color: var(--primary);
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# الواجهة الرئيسية
st.markdown('<div class="header"><h1>⬇️ نظام التحميل الطبي</h1></div>', unsafe_allow_html=True)

# حقل إدخال الرابط
url = st.text_input("", placeholder="الصق رابط يوتيوب هنا", label_visibility="collapsed")

# خيارات التحميل
col1, col2 = st.columns(2)
with col1:
    format_option = st.radio("النوع:", ["🎥 فيديو", "🎵 صوت"])
with col2:
    quality = st.selectbox("الجودة:", ["أفضل جودة", "عالية", "متوسطة"])

# زر التحميل
if st.button("تحميل الآن", use_container_width=True):
    if not url.strip():
        st.warning("يجب إدخال رابط يوتيوب صحيح")
    else:
        with st.spinner("جاري التحميل..."):
            try:
                uid = str(uuid.uuid4())
                os.makedirs("downloads", exist_ok=True)
                
                if format_option == "🎥 فيديو":
                    quality_map = {
                        "أفضل جودة": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                        "عالية": "22",
                        "متوسطة": "18"
                    }
                    cmd = f'yt-dlp -f "{quality_map[quality]}" --merge-output-format mp4 -o "downloads/{uid}.%(ext)s" "{url}"'
                else:
                    quality_map = {
                        "أفضل جودة": "bestaudio",
                        "عالية": "--audio-quality 320K",
                        "متوسطة": "--audio-quality 192K"
                    }
                    cmd = f'yt-dlp -x --audio-format mp3 {quality_map[quality]} -o "downloads/{uid}.%(ext)s" "{url}"'
                
                subprocess.run(cmd, shell=True, check=True)
                
                # البحث عن الملف المحمل
                downloaded_files = glob.glob(f"downloads/{uid}.*")
                if downloaded_files:
                    file_path = downloaded_files[0]
                    with open(file_path, "rb") as f:
                        st.success("تم التحميل بنجاح!")
                        st.download_button(
                            "حفظ الملف",
                            data=f,
                            file_name=os.path.basename(file_path),
                            use_container_width=True
                        )
                    os.remove(file_path)
                else:
                    st.error("حدث خطأ أثناء التحميل")
                    
            except subprocess.CalledProcessError as e:
                st.error(f"خطأ في التحميل: {e.stderr}")
            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {e}")

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--primary);">
    <p>نظام التحميل الطبي © 2025</p>
    <p>طور بواسطة طالب الأنظمة الطبية</p>
    <p>الدعم: <a href="mailto:rshqrwsy@gmail.com" style="color: var(--secondary);">rshqrwsy@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)