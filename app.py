import streamlit as st
import subprocess
import os
import uuid

st.set_page_config(page_title="المبرمجون الأحرار – YouTube Downloader", layout="centered", page_icon="📥")
st.title("📥 المبرمجون الأحرار – تحميل من YouTube")

url = st.text_input("أدخل رابط الفيديو:", placeholder="https://www.youtube.com/watch?v=xxxx")
format_option = st.radio("اختر الصيغة:", ["📺 فيديو", "🎵 صوت (MP3)"])
quality = st.selectbox("الجودة:", ["best", "1080p", "720p", "480p", "360p"])

if st.button("ابدأ التحميل"):
    if not url.strip():
        st.warning("⚠️ الرجاء إدخال رابط صحيح")
    else:
        uid = str(uuid.uuid4())
        template = f"{uid}.%(ext)s"
        if format_option == "📺 فيديو":
            cmd = f'yt-dlp -f "{quality}+bestaudio/best" -o "{template}" "{url}"'
        else:
            cmd = f'yt-dlp -f "bestaudio" -x --audio-format mp3 -o "{template}" "{url}"'
        with st.spinner("⏳ جاري التحميل..."):
            try:
                subprocess.run(cmd, shell=True, check=True)
                for fname in os.listdir():
                    if fname.startswith(uid):
                        with open(fname, "rb") as f:
                            st.success("✅ تم التحميل بنجاح!")
                            st.download_button("📂 حمّل الملف", data=f, file_name=fname)
                        break
            except Exception as err:
                st.error(f"❌ خطأ: {err}")
