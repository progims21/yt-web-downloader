import streamlit as st
import subprocess
import os
import uuid
import glob
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="المبرمجون الأحرار – YouTube Downloader Pro",
    layout="centered",
    page_icon="📥",
    initial_sidebar_state="expanded"
)

# تحسينات الواجهة مع تنسيق متكامل
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stDownloadButton>button {
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# هيكل الصفحة الرئيسية
st.title("📥 المبرمجون الأحرار – أداة التحميل المتقدمة")
st.markdown("""
أداة متكاملة لتحميل الفيديوهات والموسيقى من YouTube بجودة عالية مع خيارات متقدمة.
""")

# شريط جانبي للإعدادات المتقدمة
with st.sidebar:
    st.header("⚙️ الإعدادات المتقدمة")
    output_dir = st.text_input("مسار الحفظ:", "downloads")
    max_retries = st.number_input("عدد محاولات إعادة التحميل:", min_value=1, max_value=10, value=3)
    st.markdown("---")
    st.markdown("**الإصدار 2.0**")
    st.markdown("تم التطوير بواسطة المبرمجون الأحرار")

# قسم الإدخال الرئيسي
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("أدخل رابط الفيديو أو القائمة التشغيلية:", placeholder="https://www.youtube.com/...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 التحقق من الرابط"):
            if url.strip():
                st.session_state.verified = True
                st.success("✔ الرابط صالح")
            else:
                st.warning("⚠ الرجاء إدخال رابط")

# خيارات التحميل
with st.expander("🎚 خيارات التحميل", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        format_option = st.radio("نوع الملف:", ["📺 فيديو", "🎵 صوت (MP3)", "🎞 صوت وفيديو منفصلين"])
    
    with col2:
        if format_option == "📺 فيديو":
            quality = st.selectbox("جودة الفيديو:", ["أفضل جودة متاحة", "4K (2160p)", "1080p", "720p", "480p", "360p"])
        else:
            quality = st.selectbox("جودة الصوت:", ["أفضل جودة", "320 كيلوبت/ثانية", "256 كيلوبت/ثانية", "192 كيلوبت/ثانية"])
    
    with col3:
        custom_name = st.text_input("اسم مخصص للملف (اختياري):", placeholder="my_video")

# زر التحميل الرئيسي
if st.button("🚀 بدء التحميل الآن", use_container_width=True, type="primary"):
    if not url.strip():
        st.warning("⚠ الرجاء إدخال رابط صحيح")
    else:
        uid = str(uuid.uuid4())
        os.makedirs(output_dir, exist_ok=True)
        
        # بناء اسم الملف
        if custom_name:
            template = f"{output_dir}/{custom_name}.%(ext)s"
        else:
            template = f"{output_dir}/{uid}.%(ext)s"
        
        # بناء أمر التنزيل بناءً على الخيارات
        try:
            with st.spinner("⏳ جاري معالجة طلبك... الرجاء الانتظار"):
                # سجل المحاولات
                attempts = 0
                success = False
                
                while attempts < max_retries and not success:
                    attempts += 1
                    try:
                        if format_option == "📺 فيديو":
                            quality_map = {
                                "أفضل جودة متاحة": "bestvideo+bestaudio/best",
                                "4K (2160p)": "313+bestaudio/308+bestaudio",
                                "1080p": "137+bestaudio/248+bestaudio",
                                "720p": "22",
                                "480p": "135+bestaudio/244+bestaudio",
                                "360p": "18"
                            }
                            cmd = f'yt-dlp -f "{quality_map[quality]}" --merge-output-format mp4 -o "{template}" "{url}"'
                        elif format_option == "🎵 صوت (MP3)":
                            quality_map = {
                                "أفضل جودة": "bestaudio",
                                "320 كيلوبت/ثانية": "--audio-quality 320K",
                                "256 كيلوبت/ثانية": "--audio-quality 256K",
                                "192 كيلوبت/ثانية": "--audio-quality 192K"
                            }
                            cmd = f'yt-dlp -x --audio-format mp3 {quality_map[quality]} -o "{template}" "{url}"'
                        else:
                            cmd = f'yt-dlp -f "bestvideo+bestaudio" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
                        
                        # تنفيذ الأمر
                        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                        success = True
                        
                        # معالجة الملف المحمل
                        if format_option != "🎞 صوت وفيديو منفصلين":
                            downloaded_files = glob.glob(f"{output_dir}/{custom_name}.*" if custom_name else f"{output_dir}/{uid}.*")
                            if downloaded_files:
                                file_path = downloaded_files[0]
                                file_name = os.path.basename(file_path)
                                
                                with open(file_path, "rb") as f:
                                    st.success(f"✅ تم التحميل بنجاح! (المحاولة {attempts})")
                                    st.balloons()
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.download_button(
                                            "📥 حمّل الملف الآن",
                                            data=f,
                                            file_name=file_name,
                                            use_container_width=True
                                        )
                                    with col2:
                                        st.write(f"**حجم الملف:** {os.path.getsize(file_path)/1024/1024:.2f} MB")
                                        st.write(f"**وقت التحميل:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                                
                                # حذف الملف المؤقت
                                os.remove(file_path)
                            else:
                                st.error("❌ لم يتم العثور على الملف المحمل")
                        else:
                            st.success("✅ تم تحميل الملفات بنجاح في مجلد التنزيلات")
                            st.info("تم حفظ ملفات الفيديو والصوت بشكل منفصل في المجلد المحدد")
                    
                    except subprocess.CalledProcessError as e:
                        if attempts >= max_retries:
                            st.error(f"❌ فشل التحميل بعد {max_retries} محاولات. الخطأ: {e.stderr}")
                        else:
                            st.warning(f"⚠ المحاولة {attempts} فشلت، جاري إعادة المحاولة...")
                            continue
                
        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")

# قسم سجل التحميلات
if st.checkbox("عرض سجل التحميلات"):
    if os.path.exists(output_dir) and os.listdir(output_dir):
        st.subheader("📜 الملفات المحملة مسبقاً")
        files = os.listdir(output_dir)
        for file in files:
            file_path = os.path.join(output_dir, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            st.write(f"- **{file}** (آخر تعديل: {file_time})")
    else:
        st.info("لا توجد ملفات محملة مسبقاً")

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p><strong>المبرمجون الأحرار - YouTube Downloader Pro</strong></p>
    <p>الإصدار 2.0 | © 2023 جميع الحقوق محفوظة</p>
    <p>للتواصل: <a href="mailto:support@freeprogrammers.com">support@freeprogrammers.com</a></p>
</div>
""", unsafe_allow_html=True)