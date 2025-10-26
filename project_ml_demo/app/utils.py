import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
import json
def generate_and_train_model():
    """
    Sinh dữ liệu giả lập, huấn luyện mô hình hồi quy tuyến tính,
    đánh giá và lưu mô hình.
    """
    # --- 1. Sinh dữ liệu giả lập ---
    np.random.seed(42)
    num_students = 500

    data = {
        'study_hours': np.random.uniform(0, 20, num_students),
        'attendance_rate': np.random.uniform(50, 100, num_students),
        'assignment_completion': np.random.uniform(50, 100, num_students),
        'internet_use': np.random.uniform(0, 10, num_students),
        'motivation': np.random.randint(1, 6, num_students),
        'family_support': np.random.randint(1, 6, num_students),
        'stress_level': np.random.randint(1, 6, num_students),
        'part_time_hours': np.random.uniform(0, 20, num_students),
    }
    df = pd.DataFrame(data)

    # Tạo biến mục tiêu (analytic_score) dựa trên công thức
    noise = np.random.normal(0, 0.5, num_students)
    df['analytic_score'] = (
        0.25 * df['study_hours'] +
        0.03 * df['attendance_rate'] +
        0.02 * df['assignment_completion'] +
        0.1 * df['internet_use'] +
        0.5 * df['motivation'] +
        0.3 * df['family_support'] -
        0.4 * df['stress_level'] -
        0.05 * df['part_time_hours'] +
        noise
    )

    # Giới hạn điểm từ 0 đến 10
    df['analytic_score'] = np.clip(df['analytic_score'], 0, 10)

    # --- 2. Lưu dữ liệu ---
    # Tạo thư mục 'data' nếu chưa tồn tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    data_path = os.path.join(data_dir, 'synthetic_data.csv')
    df.to_csv(data_path, index=False)
    print(f"Dữ liệu đã được sinh và lưu tại: {data_path}")

    # --- 3. Huấn luyện mô hình ---
    X = df.drop('analytic_score', axis=1)
    y = df['analytic_score']

    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Huấn luyện mô hình Linear Regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Đã huấn luyện xong mô hình Linear Regression.")

    # --- 4. Đánh giá mô hình ---
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n--- Kết quả đánh giá mô hình ---")
    print(f"R-squared (R²): {r2:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print("---------------------------------")

    # --- 5. Lưu mô hình và các chỉ số ---
    model_dir = os.path.join(project_root, 'model')
    os.makedirs(model_dir, exist_ok=True)

    # Lưu mô hình
    model_path = os.path.join(model_dir, 'regression_model.pkl')
    joblib.dump(model, model_path)
    print(f"Mô hình đã được lưu tại: {model_path}")

    # Lưu các chỉ số đánh giá
    metrics = {
        'r2_score': float(r2),
        'mae': float(mae),
        'rmse': float(rmse)
    }
    metrics_path = os.path.join(model_dir, 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Các chỉ số đánh giá đã được lưu tại: {metrics_path}")


if __name__ == "__main__":
    generate_and_train_model()
