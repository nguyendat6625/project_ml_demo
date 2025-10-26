# Ứng dụng Dự báo Điểm môn Giải tích (Analytic Score Predictor)

Đây là một ứng dụng Streamlit sử dụng mô hình hồi quy tuyến tính để dự báo điểm môn Toán Giải tích của sinh viên dựa trên các yếu tố về hành vi và thói quen học tập.

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
