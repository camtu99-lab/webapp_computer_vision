# Hệ thống Nhận dạng Ngôn ngữ Ký hiệu Việt Nam — Streamlit

Chuyển đổi toàn bộ ứng dụng desktop gốc (PyQt5 + webcam) sang **web app Streamlit đa trang**,
chạy được trên máy cá nhân hoặc triển khai lên server/cloud (Streamlit Community Cloud, v.v.)

## Cấu trúc dự án

```
streamlit_app/
├── app.py                          # Trang chủ + trạng thái hệ thống
├── config.py                       # Cấu hình (tương đương config.py gốc)
├── requirements.txt
├── .env.example                    # Đổi tên thành .env và điền GEMINI_API_KEY
├── pages/
│   ├── 1_🎥_Nhan_Dang.py           # Nhận dạng thời gian thực (main.py)
│   ├── 2_📸_Thu_Thap_Du_Lieu.py    # Thu thập dữ liệu (capture_pose_data*.py)
│   ├── 3_🧠_Huan_Luyen_Mo_Hinh.py  # Huấn luyện mô hình (trainCNN3D.py)
│   └── 4_✏️_Chinh_Sua_Mapping.py   # Sửa tên nhãn (edit_model.py)
├── utils/
│   ├── feature_extraction.py       # Trích đặc trưng MediaPipe
│   ├── model.py                    # Load & dự đoán model
│   ├── capture.py                  # Logic thu thập dữ liệu
│   ├── train.py                    # Logic huấn luyện
│   ├── tao_cau.py                  # Ghép câu (Gemini API)
│   └── speak.py                    # Đọc to (gTTS — thay pyttsx3)
├── data/QIPEDC/                    # Nơi lưu các file .npy
└── models/                         # Nơi lưu model .keras + mapping .pkl
```

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Đổi tên `.env.example` thành `.env` và điền khoá Gemini API (lấy miễn phí tại
https://aistudio.google.com/app/apikey), hoặc nhập trực tiếp vào ô ở sidebar khi chạy app.

## Chạy ứng dụng

```bash
streamlit run app.py
```

Trình duyệt sẽ tự mở tại `http://localhost:8501`.

## Quy trình sử dụng đề xuất

1. **📸 Thu thập dữ liệu** — tải video/ảnh ký hiệu lên, tạo file `.npy` cho từng lớp
   (hoặc tải hàng loạt một bộ dataset dạng `train/<tên_lớp>/*.mp4`)
2. **🧠 Huấn luyện mô hình** — bấm 1 nút để huấn luyện, xem báo cáo, tải model về
3. **✏️ Chỉnh sửa mapping** (tuỳ chọn) — đổi tên hiển thị cho từng nhãn cho thân thiện hơn
4. **🎥 Nhận dạng** — bật webcam, nhận dạng ký hiệu thời gian thực, ghép câu, đọc to

## Khác biệt so với bản gốc (desktop)

| Bản gốc | Bản Streamlit |
|---|---|
| `cv2.VideoCapture(0)` + `cv2.imshow()` | `streamlit-webrtc` — truy cập webcam qua trình duyệt (WebRTC), chạy được cả khi deploy lên server |
| Giao diện PyQt5 | Giao diện web Streamlit đa trang |
| `pyttsx3` (loa hệ thống) | `gTTS` — tạo file mp3, phát qua `st.audio()` trong trình duyệt |
| Chạy 1 máy, 1 người dùng | Có thể deploy để nhiều người dùng truy cập qua trình duyệt |

## Lưu ý khi triển khai (deploy)

- `streamlit-webrtc` cần HTTPS khi deploy công khai (Streamlit Community Cloud tự có HTTPS).
- Với dataset lớn, nên dùng dịch vụ lưu trữ ngoài (S3, Google Cloud Storage...) thay vì lưu trực tiếp
  trong thư mục ứng dụng, vì nhiều nền tảng cloud có bộ nhớ tạm thời (ephemeral storage).
- `tensorflow` khá nặng — nếu deploy lên Streamlit Community Cloud (free tier), cân nhắc dùng
  `tensorflow-cpu` trong `requirements.txt` để giảm dung lượng cài đặt.
