import streamlit as st
import pickle
import os
import requests

# ฟังก์ชันดาวน์โหลดจาก Google Drive
def download_file_from_google_drive(file_id, destination):
    st.info("⏳ กำลังดาวน์โหลดข้อมูล... (ครั้งแรกอาจใช้เวลา 1-2 นาที)")
    
    URL = "https://drive.google.com/uc?export=download&confirm=1"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    # ดาวน์โหลดเป็น chunks
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
    
    st.success("✅ ดาวน์โหลดข้อมูลสำเร็จ!")

# ตรวจสอบและ import function
try:
    from myfunction_66130701931 import get_movie_recommendations
except ImportError as e:
    st.error(f"❌ ไม่สามารถ import ฟังก์ชันได้: {e}")
    st.info("กรุณาตรวจสอบว่าไฟล์ 'myfunction_66130701931.py' อยู่ในโฟลเดอร์เดียวกัน")
    st.stop()

# ตรวจสอบและโหลดข้อมูล
@st.cache_data
def load_data():
    try:
        # ตรวจสอบว่ามีไฟล์หรือยัง
        if not os.path.exists('recommendation_data.pkl'):
            # Google Drive File ID จาก link ของคุณ
            file_id = "1VBosaUXem8RmOIJPQlb09vXhv_H8fYMV"
            download_file_from_google_drive(file_id, 'recommendation_data.pkl')
        
        # โหลดไฟล์
        with open('recommendation_data.pkl', 'rb') as file:
            user_similarity_df, user_movie_ratings = pickle.load(file)
        return user_similarity_df, user_movie_ratings
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
        st.stop()

# โหลดข้อมูล
user_similarity_df, user_movie_ratings = load_data()

# Streamlit App
st.title("🎬 Movie Recommendation System")

# แสดงข้อมูล User IDs ที่มีอยู่
available_users = user_movie_ratings.index.tolist()
min_user_id = int(min(available_users))
max_user_id = int(max(available_users))

st.info(f"📊 User ID ที่มีในระบบ: {min_user_id} - {max_user_id}")

user_id = st.number_input(
    "Enter User ID:",
    min_value=min_user_id,
    max_value=max_user_id,
    value=min_user_id,
    step=1
)

if st.button("Get Recommendations"):
    try:
        # ตรวจสอบว่า User ID มีอยู่จริง
        if user_id not in available_users:
            st.error(f"❌ ไม่พบ User ID {user_id} ในระบบ")
            st.info(f"กรุณาเลือก User ID ระหว่าง {min_user_id} - {max_user_id}")
        else:
            with st.spinner('กำลังค้นหาหนังแนะนำ...'):
                recommendations = get_movie_recommendations(
                    user_id,
                    user_similarity_df,
                    user_movie_ratings,
                    10
                )
            
            if recommendations is not None and len(recommendations) > 0:
                st.success(f"✅ พบหนังแนะนำสำหรับ User {user_id}")
                st.subheader(f"🎬 Top 10 movie recommendations for User {user_id}:")
                for idx, movie_title in enumerate(recommendations, 1):
                    st.write(f"{idx}. {movie_title}")
            else:
                st.warning("⚠️ ไม่พบหนังที่จะแนะนำสำหรับ User นี้")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
        st.info("กรุณาตรวจสอบ function get_movie_recommendations")

# เพิ่มข้อมูลเกี่ยวกับระบบ
with st.expander("ℹ️ ข้อมูลระบบ"):
    st.write(f"- จำนวน Users ทั้งหมด: {len(available_users)}")
    st.write(f"- จำนวนหนังทั้งหมด: {user_movie_ratings.shape[1]}")
    st.write(f"- รูปแบบ User Similarity: {user_similarity_df.shape}")
