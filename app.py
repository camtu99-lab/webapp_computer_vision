import glob
import os

import streamlit as st
from dotenv import load_dotenv

from config import DATA_DIR, MODEL_DIR, MODEL_NAME

load_dotenv()

st.set_page_config(
    page_title="Nhận dạng Ngôn ngữ Ký hiệu Việt Nam",
    page_icon="🤟",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar — cấu hình chung dùng xuyên suốt ứng dụng
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Cấu hình")

    gemini_key_input = st.text_input(
        "Gemini API Key (để ghép câu)",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Lấy miễn phí tại https://aistudio.google.com/app/apikey",
    )
    if gemini_key_input:
        os.environ["GEMINI_API_KEY"] = gemini_key_input

    st.divider()
    st.caption("📁 Đường dẫn dữ liệu")
    st.code(f"DATA_DIR  = {DATA_DIR}\nMODEL_DIR = {MODEL_DIR}", language="text")

# ---------------------------------------------------------------------------
# Trang chủ
# ---------------------------------------------------------------------------
st.title("🤟 Hệ thống Nhận dạng Ngôn ngữ Ký hiệu Việt Nam")

st.markdown(
    """
Chào mừng bạn đến với hệ thống web **nhận dạng ngôn ngữ ký hiệu** — chuyển đổi toàn bộ
ứng dụng desktop (PyQt5 + webcam) gốc sang giao diện web Streamlit, chạy được cả trên máy cá nhân
lẫn triển khai lên server/cloud.

👈 **Chọn 1 trang ở thanh bên trái** để bắt đầu:

| Trang | Chức năng | Tương đương file gốc |
|---|---|---|
| 🎥 Nhận dạng | Bật webcam, nhận dạng ký hiệu thời gian thực, ghép câu, đọc to | `main.py` |
| 📸 Thu thập dữ liệu | Tải lên ảnh/video, trích đặc trưng, lưu thành `.npy` | `capture_pose_data.py`, `capture_pose_data_video.py` |
| 🧠 Huấn luyện mô hình | Huấn luyện CNN 3D từ dữ liệu `.npy`, xem báo cáo, tải model về | `scripts/trainCNN3D.py`, `mainTrainUser.py` |
| ✏️ Chỉnh sửa mapping | Sửa tên hiển thị ứng với từng nhãn lớp | `edit_model.py` |
"""
)

st.divider()

# ---------------------------------------------------------------------------
# Trạng thái hệ thống
# ---------------------------------------------------------------------------
st.subheader("📊 Trạng thái hệ thống")

col1, col2, col3 = st.columns(3)

npy_files = glob.glob(os.path.join(DATA_DIR, "*.npy"))
with col1:
    st.metric("Số lớp dữ liệu (.npy)", len(npy_files))

model_path = os.path.join(MODEL_DIR, f"{MODEL_NAME}.keras")
with col2:
    st.metric("Mô hình đã huấn luyện", "Có ✅" if os.path.exists(model_path) else "Chưa ❌")

with col3:
    st.metric("Gemini API Key", "Đã cấu hình ✅" if os.getenv("GEMINI_API_KEY") else "Chưa cấu hình ❌")

if not npy_files:
    st.info("Chưa có dữ liệu `.npy` nào. Hãy sang trang **📸 Thu thập dữ liệu** để tạo dữ liệu trước.")
if not os.path.exists(model_path):
    st.info("Chưa có mô hình đã huấn luyện. Hãy sang trang **🧠 Huấn luyện mô hình** sau khi có dữ liệu.")
