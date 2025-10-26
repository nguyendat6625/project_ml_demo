# 🔧 Hướng dẫn Troubleshooting

## Các vấn đề thường gặp và cách giải quyết

### 1. Build Failed trên Render

#### Lỗi: `ModuleNotFoundError: No module named 'streamlit'`

**Nguyên nhân**: Dependencies không được cài đặt

**Giải pháp**:
```bash
# Kiểm tra requirements.txt có tất cả packages
cat requirements.txt

# Cập nhật requirements.txt
pip freeze > requirements.txt
```

#### Lỗi: `Python version not supported`

**Nguyên nhân**: Python version không tương thích

**Giải pháp**:
- Kiểm tra `runtime.txt` có đúng format: `python-3.11.6`
- Render hỗ trợ Python 3.7 - 3.11

#### Lỗi: `Build command failed`

**Giải pháp**:
1. Xem logs chi tiết
2. Kiểm tra `Procfile` hoặc `render.yaml`
3. Đảm bảo `app/utils.py` chạy được locally

---

### 2. Application Crashed

#### Lỗi: `FileNotFoundError: [Errno 2] No such file or directory`

**Nguyên nhân**: Đường dẫn file không chính xác

**Giải pháp**:
- Sử dụng `os.path.abspath()` thay vì hardcode paths
- Kiểm tra file tồn tại trước khi load
- Sử dụng `os.path.join()` cho cross-platform compatibility

```python
# ✅ Đúng
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '../data', 'file.csv')

# ❌ Sai
file_path = '../data/file.csv'
```

#### Lỗi: `Port already in use`

**Nguyên nhân**: Port 8501 đã được sử dụng

**Giải pháp**:
- Render tự động gán port
- Đảm bảo start command có `--server.port=$PORT`

#### Lỗi: `Memory exceeded`

**Nguyên nhân**: Ứng dụng sử dụng quá nhiều RAM

**Giải pháp**:
- Tối ưu hóa model size
- Sử dụng caching trong Streamlit
- Giảm kích thước dữ liệu

---

### 3. Lỗi khi chạy locally

#### Lỗi: `ModuleNotFoundError`

**Giải pháp**:
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc cài đặt từng package
pip install streamlit pandas numpy scikit-learn plotly joblib
```

#### Lỗi: `No such file or directory: '../data/synthetic_data.csv'`

**Giải pháp**:
```bash
# Chạy utils.py để tạo dữ liệu
python app/utils.py

# Sau đó chạy app
streamlit run app/app.py
```

#### Lỗi: `Permission denied`

**Giải pháp** (Windows):
```bash
# Chạy PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 4. Lỗi khi push lên GitHub

#### Lỗi: `fatal: not a git repository`

**Giải pháp**:
```bash
# Khởi tạo git
git init

# Cấu hình git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Lỗi: `remote origin already exists`

**Giải pháp**:
```bash
# Xóa remote cũ
git remote remove origin

# Thêm remote mới
git remote add origin https://github.com/YOUR_USERNAME/repo.git
```

#### Lỗi: `fatal: 'origin' does not appear to be a 'git' repository`

**Giải pháp**:
```bash
# Kiểm tra remote
git remote -v

# Thêm remote nếu chưa có
git remote add origin https://github.com/YOUR_USERNAME/repo.git
```

---

### 5. Lỗi khi deploy lên Render

#### Lỗi: `Build log is empty`

**Giải pháp**:
- Chờ vài giây, logs sẽ xuất hiện
- Refresh page
- Kiểm tra kết nối internet

#### Lỗi: `Deployment failed`

**Giải pháp**:
1. Xem logs chi tiết
2. Kiểm tra build command
3. Kiểm tra start command
4. Đảm bảo repository public

#### Lỗi: `Application not responding`

**Giải pháp**:
- Ứng dụng có thể đang spin up (cold start)
- Chờ 30-60 giây
- Refresh page
- Kiểm tра logs để xem lỗi

---

### 6. Lỗi liên quan đến Streamlit

#### Lỗi: `streamlit.errors.StreamlitAPIException`

**Giải pháp**:
- Kiểm tra syntax Streamlit code
- Đảm bảo không có lỗi Python
- Xem logs để xem chi tiết

#### Lỗi: `Cache not working`

**Giải pháp**:
```python
# Sử dụng @st.cache_resource cho objects
@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

# Sử dụng @st.cache_data cho data
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')
```

---

### 7. Lỗi liên quan đến dữ liệu

#### Lỗi: `ValueError: could not convert string to float`

**Giải pháp**:
- Kiểm tra định dạng dữ liệu
- Đảm bảo CSV có đúng encoding
- Sử dụng `encoding='utf-8'` khi read CSV

```python
df = pd.read_csv('file.csv', encoding='utf-8')
```

#### Lỗi: `KeyError: 'column_name'`

**Giải pháp**:
- Kiểm tra tên cột đúng
- Sử dụng `df.columns` để xem tất cả cột
- Kiểm tra dữ liệu được load đúng

---

## 📋 Checklist Debug

- [ ] Kiểm tra logs (Render dashboard → Logs)
- [ ] Kiểm tra file paths (sử dụng absolute paths)
- [ ] Kiểm tra requirements.txt (có tất cả packages)
- [ ] Kiểm tra Python version (3.8+)
- [ ] Kiểm tra environment variables
- [ ] Kiểm tra permissions (file readable/writable)
- [ ] Kiểm tra internet connection
- [ ] Kiểm tra git status (all files committed)

---

## 🆘 Nếu vẫn không giải quyết được

1. **Xem logs chi tiết**:
   - Render: Dashboard → Logs
   - Local: Terminal output

2. **Tìm kiếm lỗi**:
   - Google: `[error message] streamlit`
   - Stack Overflow: Tag `streamlit`
   - GitHub Issues: `streamlit/streamlit`

3. **Tạo issue**:
   - Mô tả lỗi chi tiết
   - Kèm logs
   - Kèm steps to reproduce
   - Kèm environment info

---

## 📞 Liên hệ hỗ trợ

- **Streamlit**: https://discuss.streamlit.io
- **Render**: https://render.com/docs
- **GitHub**: Tạo issue trên repository

---

**Chúc bạn giải quyết vấn đề thành công! 💪**
