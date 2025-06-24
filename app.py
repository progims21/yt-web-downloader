import streamlit as st
import subprocess
import os
import uuid
import glob
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="نظام تحميل الفيديوهات الطبي",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### نظام تطويري من إعداد طالب الأنظمة الطبية\nللدعم الفني: rshqrwsy@gmail.com"
    }
)

# تنسيقات CSS مخصصة
st.markdown("""
<style>
    :root {
        --primary: #2E86AB;
        --secondary: #F18F01;
        --accent: #C73E1D;
        --background: #F5F5F5;
        --card: #FFFFFF;
    }
    
    .stApp {
        background-color: var(--background);
    }
    
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary);
        transform: scale(1.05);
    }
    
    .stDownloadButton>button {
        background-color: var(--accent);
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
    }
    
    .css-1aumxhk {
        background-color: var(--card);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .header {
        color: var(--primary);
        text-align: center;
        margin-bottom: 30px;
    }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# هيكل الصفحة الرئيسية
st.markdown('<div class="header"><h1>🎬 نظام تحميل الفيديوهات الطبي المتكامل</h1></div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <h3>أهلاً بك في نظام تحميل الفيديوهات المتقدم</h3>
    <p>أداة متكاملة لتحميل المحتوى التعليمي والطبي من يوتيوب بجودة عالية مع دعم الصوت والفيديو</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=100)

# شريط جانبي للإعدادات
with st.sidebar:
    st.markdown("""
    <div style="text-align: center;">
    <h2>⚙️ الإعدادات الفنية</h2>
    </div>
    """, unsafe_allow_html=True)
    
    output_dir = st.text_input("مسار حفظ الملفات:", "downloads")
    max_retries = st.number_input("عدد المحاولات عند الخطأ:", min_value=1, max_value=10, value=3)
    st.markdown("---")
    st.markdown("**الإصدار 3.0**")
    st.markdown("**المؤسس:** طالب الأنظمة الطبية")
    st.markdown("**الدعم الفني:** [rshqrwsy@gmail.com](mailto:rshqrwsy@gmail.com)")

# قسم الإدخال الرئيسي
with st.container():
    st.markdown("### أدخل رابط الفيديو أو المحاضرة")
    url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

# خيارات التحميل
with st.expander("⚙️ خيارات التحميل المتقدمة", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        format_option = st.radio("نوع الملف:", ["🎥 فيديو كامل (بصوت)", "🎵 صوت فقط (MP3)", "📼 فيديو عالي الجودة"])
        
    with col2:
        if format_option == "🎥 فيديو كامل (بصوت)":
            quality = st.selectbox("جودة الفيديو:", ["أفضل جودة", "1080p (FHD)", "720p (HD)", "480p (SD)"])
        elif format_option == "📼 فيديو عالي الجودة":
            quality = st.selectbox("جودة الفيديو:", ["4K (UHD)", "1440p (QHD)", "1080p (FHD)"])
        else:
            quality = st.selectbox("جودة الصوت:", ["أفضل جودة (320kbps)", "جودة عالية (256kbps)", "جودة متوسطة (192kbps)"])

    custom_name = st.text_input("اسم مخصص للملف (اختياري):", placeholder="مثال: محاضرة_القلب_2025")

# زر التحميل الرئيسي
if st.button("🚀 بدء عملية التحميل", use_container_width=True, type="primary"):
    if not url.strip():
        st.error("⚠️ يرجى إدخال رابط صحيح")
    else:
        uid = str(uuid.uuid4())
        os.makedirs(output_dir, exist_ok=True)
        
        # بناء اسم الملف
        if custom_name:
            template = f"{output_dir}/{custom_name}.%(ext)s"
        else:
            template = f"{output_dir}/%(title)s.%(ext)s"
        
        # بناء أمر التنزيل
        try:
            with st.spinner("⏳ جاري معالجة طلبك، قد تستغرق العملية عدة دقائق..."):
                attempts = 0
                success = False
                
                while attempts < max_retries and not success:
                    attempts += 1
                    try:
                        if format_option == "🎥 فيديو كامل (بصوت)":
                            quality_map = {
                                "أفضل جودة": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                                "1080p (FHD)": "137+140",
                                "720p (HD)": "22",
                                "480p (SD)": "135+140"
                            }
                            cmd = f'yt-dlp -f "{quality_map[quality]}" --merge-output-format mp4 -o "{template}" "{url}"'
                        
                        elif format_option == "📼 فيديو عالي الجودة":
                            quality_map = {
                                "4K (UHD)": "313+251",
                                "1440p (QHD)": "271+251",
                                "1080p (FHD)": "137+251"
                            }
                            cmd = f'yt-dlp -f "{quality_map[quality]}" --merge-output-format mp4 -o "{template}" "{url}"'
                        
                        else:  # صوت فقط
                            quality_map = {
                                "أفضل جودة (320kbps)": "-x --audio-format mp3 --audio-quality 320K",
                                "جودة عالية (256kbps)": "-x --audio-format mp3 --audio-quality 256K",
                                "جودة متوسطة (192kbps)": "-x --audio-format mp3 --audio-quality 192K"
                            }
                            cmd = f'yt-dlp {quality_map[quality]} -o "{template}" "{url}"'
                        
                        # تنفيذ الأمر مع التحقق من وجود الصوت
                        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                        
                        # التحقق من وجود الصوت في ملفات الفيديو
                        if format_option != "🎵 صوت فقط (MP3)":
                            if custom_name:
                                file_pattern = f"{output_dir}/{custom_name}.*"
                            else:
                                file_pattern = f"{output_dir}/*.mp4"
                            
                            downloaded_files = glob.glob(file_pattern)
                            if downloaded_files:
                                file_path = max(downloaded_files, key=os.path.getctime)
                                
                                # التحقق من وجود تيار صوتي في الفيديو
                                check_audio = f'ffprobe -i "{file_path}" -show_streams -select_streams a -loglevel error'
                                audio_check = subprocess.run(check_audio, shell=True, capture_output=True, text=True)
                                
                                if audio_check.returncode != 0 or not audio_check.stdout:
                                    st.warning("⚠️ تم تحميل الفيديو بدون صوت، جاري إعادة المحاولة...")
                                    os.remove(file_path)
                                    continue
                                
                                success = True
                                file_name = os.path.basename(file_path)
                                
                                with open(file_path, "rb") as f:
                                    st.success("✅ تم التحميل بنجاح!")
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
                                        file_size = os.path.getsize(file_path)/1024/1024
                                        st.metric("حجم الملف", f"{file_size:.2f} MB")
                                        st.metric("مدة المعالجة", f"{attempts} محاولة")
                                
                                os.remove(file_path)
                            else:
                                st.error("❌ لم يتم العثور على الملف المحمل")
                        else:
                            success = True
                            st.success("✅ تم تحميل الملف الصوتي بنجاح!")
                            st.balloons()
                            audio_files = glob.glob(f"{output_dir}/*.mp3")
                            if audio_files:
                                with open(audio_files[0], "rb") as f:
                                    st.download_button(
                                        "💾 حفظ الملف الصوتي",
                                        data=f,
                                        file_name=os.path.basename(audio_files[0]),
                                        use_container_width=True
                                    )
                                os.remove(audio_files[0])
                    
                    except subprocess.CalledProcessError as e:
                        if attempts >= max_retries:
                            st.error(f"❌ فشل التحميل بعد {max_retries} محاولات.\nالخطأ: {e.stderr}")
                        else:
                            st.warning(f"🔄 المحاولة {attempts} فشلت، جاري إعادة المحاولة...")
                            continue
        
        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {str(e)}")

# قسم التعليمات
with st.expander("❓ التعليمات والإرشادات"):
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
    <h3>أسئلة شائعة:</h3>
    <ol>
        <li><strong>لماذا لا يوجد صوت في الفيديو؟</strong><br>
        النظام الآن يتأكد تلقائياً من وجود الصوت ويحاول إصلاح المشكلة عند حدوثها.</li>
        <li><strong>كيف أختار أفضل جودة؟</strong><br>
        اختر "أفضل جودة" من القائمة المنسدلة للجودة.</li>
        <li><strong>هل يمكن تحميل قوائم التشغيل؟</strong><br>
        نعم، يمكنك وضع رابط قائمة التشغيل وسيتم التعامل معها تلقائياً.</li>
        <li><strong>أين يتم حفظ الملفات؟</strong><br>
        يتم حفظها في مجلد "downloads" إلا إذا قمت بتغيير المسار في الإعدادات.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("""
<div class="footer">
    <p>نظام تحميل الفيديوهات الطبي © 2025</p>
    <p>تم التطوير بواسطة طالب الأنظمة الطبية</p>
    <p>للدعم الفني: <a href="mailto:rshqrwsy@gmail.com" style="color: white;">rshqrwsy@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)