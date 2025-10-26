# 📊 Ứng dụng Dự báo Điểm môn Giải tích (Analytic Score Predictor)

Đây là một ứng dụng Streamlit sử dụng mô hình hồi quy tuyến tính để dự báo điểm môn Toán Giải tích của sinh viên dựa trên các yếu tố về hành vi và thói quen học tập.

**🎨 Giao diện:** Thiết kế hiện đại với nhiều màu sắc, animation mượt mà, và responsive design cho cả desktop lẫn mobile.

## Cấu trúc dự án

```
analytic_score_predictor/
│
├── data/
│   └── synthetic_data.csv
│
├── model/
│   └── regression_model.pkl
│
├── app/
│   ├── app.py
│   ├── __init__.py
│   └── utils.py
│
├── requirements.txt
└── README.md
```

## Hướng dẫn cài đặt và sử dụng

### 1. Cài đặt thư viện

Đảm bảo bạn đã cài đặt Python. Sau đó, cài đặt các thư viện cần thiết bằng lệnh sau:

```bash
pip install -r requirements.txt
```

### 2. Huấn luyện mô hình

Chạy script sau để sinh dữ liệu giả lập, huấn luyện mô hình hồi quy, và lưu lại mô hình. Dữ liệu sẽ được lưu tại `data/synthetic_data.csv` và mô hình tại `model/regression_model.pkl`.

```bash
python app/utils.py
```

Sau khi chạy, bạn sẽ thấy các chỉ số đánh giá mô hình như R-squared, MAE, và RMSE được in ra trên console.

### 3. Chạy ứng dụng Streamlit

Sử dụng lệnh sau để khởi chạy ứng dụng web:

```bash
streamlit run app/app.py
```

Trình duyệt sẽ tự động mở giao diện ứng dụng. Tại đây, bạn có thể nhập các thông số và nhận kết quả dự báo điểm.

## 🚀 Deploy lên Render

### Bước 1: Push lên GitHub

```bash
# Khởi tạo git repository
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit: Analytic Score Predictor with enhanced UI"

# Thêm remote repository
git remote add origin https://github.com/YOUR_USERNAME/analytic_score_predictor.git

# Push lên GitHub
git branch -M main
git push -u origin main
```

### Bước 2: Deploy lên Render

1. Truy cập [render.com](https://render.com)
2. Đăng nhập hoặc tạo tài khoản
3. Nhấp vào **New +** → **Web Service**
4. Kết nối GitHub repository của bạn
5. Điền thông tin:
   - **Name**: `analytic-score-predictor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python app/utils.py`
   - **Start Command**: `streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0`
6. Nhấp **Create Web Service**

### Bước 3: Cấu hình Environment Variables (nếu cần)

Trong Render dashboard:
- Đi tới **Environment** tab
- Thêm biến `PYTHONUNBUFFERED=true`

### Bước 4: Kiểm tra Deployment

- Render sẽ tự động build và deploy
- Xem logs để kiểm tra lỗi
- Ứng dụng sẽ có sẵn tại: `https://your-app-name.onrender.com`

## 📋 Yêu cầu hệ thống

- Python 3.8+
- pip (Python package manager)
- Git (để push lên GitHub)

## 📦 Dependencies

Tất cả dependencies được liệt kê trong `requirements.txt` với phiên bản cụ thể để đảm bảo tính tương thích.

## 🎯 Tính năng chính

✅ Dự báo điểm dựa trên các yếu tố học tập  
✅ Giao diện hiện đại với animation mượt mà  
✅ Responsive design cho mobile và desktop  
✅ Phân tích dữ liệu chi tiết  
✅ Đánh giá hiệu suất mô hình  
✅ Hồ sơ sinh viên so sánh  

## 📝 Lưu ý

- Dữ liệu được sinh giả lập mỗi lần deploy
- Mô hình được huấn luyện tự động khi ứng dụng khởi động
- Không cần cơ sở dữ liệu bên ngoài

## 📧 Liên hệ

Nếu có bất kỳ vấn đề nào, vui lòng tạo issue trên GitHub.
