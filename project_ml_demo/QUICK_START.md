# ⚡ Quick Start Guide

## 🚀 Chạy ứng dụng locally (5 phút)

### Bước 1: Clone hoặc Download repository

```bash
# Clone từ GitHub
git clone https://github.com/YOUR_USERNAME/analytic_score_predictor.git
cd analytic_score_predictor

# Hoặc download ZIP và giải nén
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Tạo dữ liệu và mô hình

```bash
python app/utils.py
```

**Output mong đợi**:
```
Dữ liệu đã được sinh và lưu tại: ../data/synthetic_data.csv
Đã huấn luyện xong mô hình Linear Regression.

--- Kết quả đánh giá mô hình ---
R-squared (R²): 0.xxxx
Mean Absolute Error (MAE): x.xxxx
Root Mean Squared Error (RMSE): x.xxxx
---------------------------------
Mô hình đã được lưu tại: ../model/regression_model.pkl
Các chỉ số đánh giá đã được lưu tại: ../model/model_metrics.json
```

### Bước 4: Chạy ứng dụng

```bash
streamlit run app/app.py
```

**Output mong đợi**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Bước 5: Mở trình duyệt

- Nhấp vào link hoặc truy cập `http://localhost:8501`
- Ứng dụng sẽ tự động mở

---

## 📤 Deploy lên Render (10 phút)

### Bước 1: Push lên GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Bước 2: Tạo Web Service trên Render

1. Truy cập [render.com](https://render.com)
2. Đăng nhập với GitHub
3. Nhấp **New +** → **Web Service**
4. Chọn repository `analytic_score_predictor`
5. Điền:
   - **Name**: `analytic-score-predictor`
   - **Build Command**: `pip install -r requirements.txt && python app/utils.py`
   - **Start Command**: `streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0`
6. Nhấp **Create Web Service**

### Bước 3: Chờ deploy

- Render sẽ build và deploy
- Xem logs để kiểm tra tiến trình
- Khi xong, URL sẽ hiển thị

### Bước 4: Truy cập ứng dụng

- Nhấp vào URL hoặc truy cập `https://analytic-score-predictor.onrender.com`

---

## 📁 Cấu trúc thư mục

```
analytic_score_predictor/
├── app/
│   ├── app.py              ← Ứng dụng chính
│   └── utils.py            ← Script huấn luyện
├── data/
│   └── synthetic_data.csv   ← Dữ liệu (tạo tự động)
├── model/
│   ├── regression_model.pkl ← Mô hình (tạo tự động)
│   └── model_metrics.json   ← Metrics (tạo tự động)
├── .streamlit/
│   └── config.toml          ← Cấu hình Streamlit
├── requirements.txt         ← Dependencies
└── README.md                ← Hướng dẫn
```

---

## 🎯 Các tính năng chính

### 📊 Tab 1: Dự báo & Phân tích
- Nhập các thông số học tập
- Xem dự báo điểm
- So sánh với sinh viên trung bình
- Nhận khuyến nghị

### 📈 Tab 2: Khám phá Dữ liệu
- Xem thống kê dữ liệu
- Phân tích phân phối
- Ma trận tương quan

### ⚙️ Tab 3: Hiệu suất Mô hình
- Xem R², MAE, RMSE
- Hệ số ảnh hưởng của các yếu tố
- Giải thích kết quả

---

## 🎨 Giao diện

- **Màu sắc**: Cyan, Purple, Green, Red
- **Animation**: Fade-in, Gradient shift, Hover effects
- **Responsive**: Tối ưu cho desktop, tablet, mobile

---

## 🔧 Troubleshooting nhanh

| Lỗi | Giải pháp |
|-----|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `FileNotFoundError` | `python app/utils.py` |
| `Port already in use` | Đóng ứng dụng khác hoặc dùng port khác |
| `Build failed` | Xem logs, kiểm tra requirements.txt |

---

## 📚 Tài liệu thêm

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Hướng dẫn deploy chi tiết
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Giải quyết vấn đề
- [README.md](README.md) - Hướng dẫn đầy đủ
- [UI_FEATURES.md](UI_FEATURES.md) - Tính năng giao diện

---

## 💡 Tips

- Lần đầu chạy sẽ chậm hơn (tải Google Fonts)
- Render free tier có cold start (~30s)
- Dữ liệu được tạo mới mỗi lần deploy
- Không cần cơ sở dữ liệu bên ngoài

---

**Chúc bạn thành công! 🎉**
