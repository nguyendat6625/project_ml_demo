# 🚀 Hướng dẫn Deploy lên Render

## Chuẩn bị trước khi Deploy

### ✅ Checklist:

- [x] `requirements.txt` có phiên bản cụ thể
- [x] `.gitignore` được tạo
- [x] `Procfile` được tạo
- [x] `setup.sh` được tạo
- [x] `.streamlit/config.toml` được tạo
- [x] `render.yaml` được tạo
- [x] Tất cả file cần thiết trong thư mục

## Bước 1: Chuẩn bị GitHub

### 1.1 Khởi tạo Git Repository

```bash
cd g:\Programming\app-projects\analytic_score_predictor
git init
```

### 1.2 Cấu hình Git (lần đầu)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 1.3 Thêm tất cả file

```bash
git add .
```

### 1.4 Commit

```bash
git commit -m "Initial commit: Analytic Score Predictor with enhanced UI and deployment configs"
```

### 1.5 Tạo Repository trên GitHub

1. Truy cập [github.com](https://github.com)
2. Nhấp **New repository**
3. Đặt tên: `analytic_score_predictor`
4. Chọn **Public** (để Render có thể truy cập)
5. Nhấp **Create repository**

### 1.6 Push lên GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/analytic_score_predictor.git
git push -u origin main
```

## Bước 2: Deploy lên Render

### 2.1 Tạo tài khoản Render

1. Truy cập [render.com](https://render.com)
2. Nhấp **Sign up**
3. Chọn **Sign up with GitHub** (dễ hơn)
4. Authorize Render

### 2.2 Tạo Web Service

1. Từ Render dashboard, nhấp **New +**
2. Chọn **Web Service**
3. Kết nối GitHub repository:
   - Nhấp **Connect account** (nếu chưa)
   - Chọn repository `analytic_score_predictor`
   - Nhấp **Connect**

### 2.3 Cấu hình Web Service

Điền các thông tin sau:

| Trường | Giá trị |
|--------|--------|
| **Name** | `analytic-score-predictor` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python app/utils.py` |
| **Start Command** | `streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0` |
| **Instance Type** | `Free` |
| **Region** | `Singapore` (hoặc gần bạn nhất) |

### 2.4 Thêm Environment Variables

1. Scroll xuống mục **Environment**
2. Nhấp **Add Environment Variable**
3. Thêm các biến sau:

```
PYTHONUNBUFFERED=true
```

### 2.5 Deploy

1. Nhấp **Create Web Service**
2. Render sẽ bắt đầu build
3. Xem logs để kiểm tra tiến trình

## Bước 3: Kiểm tra Deployment

### 3.1 Xem Logs

- Trong Render dashboard, mở service
- Nhấp **Logs** tab
- Xem các thông báo build

### 3.2 Kiểm tra URL

- Khi build xong, URL sẽ hiển thị
- Format: `https://analytic-score-predictor.onrender.com`
- Nhấp vào để mở ứng dụng

### 3.3 Troubleshooting

**Lỗi: Build failed**
- Kiểm tra logs để xem lỗi cụ thể
- Đảm bảo `requirements.txt` có tất cả dependencies
- Kiểm tra Python version (phải >= 3.8)

**Lỗi: Application crashed**
- Xem logs để tìm nguyên nhân
- Kiểm tra file paths (sử dụng relative paths)
- Đảm bảo `app/utils.py` chạy thành công

**Lỗi: Port không khả dụng**
- Render tự động gán port
- Đảm bảo start command có `--server.port=$PORT`

## Bước 4: Cập nhật ứng dụng

Sau khi deploy, nếu bạn muốn cập nhật:

```bash
# Thay đổi file
# ...

# Commit và push
git add .
git commit -m "Update: [mô tả thay đổi]"
git push origin main
```

Render sẽ tự động rebuild và deploy phiên bản mới.

## 📊 Cấu trúc File cho Deployment

```
analytic_score_predictor/
├── .streamlit/
│   └── config.toml          # Cấu hình Streamlit
├── app/
│   ├── __init__.py
│   ├── app.py              # Ứng dụng chính
│   └── utils.py            # Script huấn luyện mô hình
├── data/
│   └── synthetic_data.csv   # Dữ liệu (được tạo tự động)
├── model/
│   ├── regression_model.pkl # Mô hình (được tạo tự động)
│   └── model_metrics.json   # Metrics (được tạo tự động)
├── .gitignore              # Git ignore file
├── Procfile                # Cấu hình Heroku/Render
├── render.yaml             # Cấu hình Render
├── setup.sh                # Setup script
├── requirements.txt        # Python dependencies
├── README.md               # Hướng dẫn sử dụng
├── CHANGELOG.md            # Lịch sử thay đổi
├── UI_FEATURES.md          # Tính năng UI
└── DEPLOYMENT_GUIDE.md     # File này
```

## 🔒 Bảo mật

- ✅ Không commit file `.env` hoặc `secrets.toml`
- ✅ Sử dụng `.gitignore` để loại trừ file nhạy cảm
- ✅ Không hardcode API keys hoặc passwords
- ✅ Render tự động HTTPS

## 📈 Monitoring

Trong Render dashboard:
- Xem **Metrics** để kiểm tra CPU, Memory, Bandwidth
- Xem **Logs** để debug lỗi
- Xem **Events** để theo dõi deployments

## 💡 Tips

1. **Free tier limitations**:
   - Ứng dụng sẽ spin down sau 15 phút không hoạt động
   - Lần truy cập đầu tiên sẽ chậm hơn (cold start)
   - Giới hạn 750 giờ/tháng

2. **Tối ưu hóa**:
   - Giữ `requirements.txt` nhỏ gọn
   - Sử dụng caching trong Streamlit
   - Tối ưu hóa model size

3. **Cập nhật thường xuyên**:
   - Kiểm tra cập nhật dependencies
   - Cập nhật Python version khi cần
   - Theo dõi security patches

## 🆘 Hỗ trợ

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Issues**: Tạo issue trên repository

---

**Chúc bạn deploy thành công! 🎉**
