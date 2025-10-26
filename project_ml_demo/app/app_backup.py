import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import numpy as np

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Dashboard Dự báo Điểm",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Tùy chỉnh cho Dark Theme chuyên nghiệp ---
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #0E1117;
        border-right: 1px solid #2E2E2E;
    }
    /* Main content containers */
    .st-emotion-cache-18e3th9 {
        background-color: #161A25;
        border: 1px solid #2A2E35;
        border-radius: 8px;
        padding: 1.5rem;
    }
    /* Metric display */
    .st-emotion-cache-176rr6j {
        background-color: #262730;
        border: 1px solid #3C3F46;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    /* Titles and headers */
    h1, h2, h3 {
        color: #00A67E; /* A vibrant accent color */
    }
    /* Buttons */
    .stButton>button {
        background-color: #00A67E;
        color: #FFFFFF;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #008765;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        border-bottom: 2px solid #262730;
    }
    .stTabs [aria-selected="true"] {
        background-color: #262730;
        border-bottom: 2px solid #00A67E;
    }
</style>
""", unsafe_allow_html=True)


# --- Các hàm tải tài nguyên ---
@st.cache_resource
def load_model():
    """Tải mô hình hồi quy."""
    model_path = os.path.join('../model', 'regression_model.pkl')
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

@st.cache_data
def load_data():
    """Tải dữ liệu huấn luyện."""
    data_path = os.path.join('../data', 'synthetic_data.csv')
    if not os.path.exists(data_path):
        return None
    return pd.read_csv(data_path)

@st.cache_data
def load_metrics():
    """Tải các chỉ số đánh giá mô hình."""
    metrics_path = os.path.join('../model', 'model_metrics.json')
    if not os.path.exists(metrics_path):
        return None
    with open(metrics_path, 'r') as f:
        return json.load(f)

# --- Tải tài nguyên ---
model = load_model()
df = load_data()
metrics = load_metrics()

# --- Sidebar ---
with st.sidebar:
    st.title("🎓 Dashboard Dự báo")
    st.markdown("Điều chỉnh các thông số đầu vào để dự báo điểm môn Giải tích của sinh viên.")

    with st.form("prediction_form"):
        st.header("Thông số đầu vào")
        study_hours = st.slider("Giờ tự học/tuần", 0.0, 20.0, 10.0, 0.5)
        attendance_rate = st.slider("Tỷ lệ chuyên cần (%)", 50.0, 100.0, 85.0)
        assignment_completion = st.slider("Tỷ lệ hoàn thành BT (%)", 50.0, 100.0, 90.0)
        internet_use = st.slider("Giờ học online/tuần", 0.0, 10.0, 5.0, 0.5)
        motivation = st.select_slider("Động lực học tập", [1, 2, 3, 4, 5], 3)
        family_support = st.select_slider("Hỗ trợ từ gia đình", [1, 2, 3, 4, 5], 4)
        stress_level = st.select_slider("Mức độ căng thẳng", [1, 2, 3, 4, 5], 2)
        part_time_hours = st.slider("Giờ làm thêm/tuần", 0.0, 20.0, 5.0, 0.5)
        submit_button = st.form_submit_button(label="🚀 Dự đoán ngay")

# --- Giao diện chính ---
if model is None or df is None or metrics is None:
    st.error("Lỗi: Không tìm thấy mô hình, dữ liệu hoặc chỉ số. Vui lòng chạy `python app/utils.py` để tạo chúng.")
else:
    st.title("📊 Dashboard Phân tích và Dự báo Điểm")
    st.markdown("Chào mừng bạn đến với dashboard tương tác. Sử dụng thanh bên trái để nhập dữ liệu và xem kết quả dự báo chi tiết tại các tab bên dưới.")

    tab1, tab2, tab3 = st.tabs(["📈 Dự báo & Phân tích", "📊 Khám phá Dữ liệu", "⚙️ Hiệu suất Mô hình"])

    # --- Tab 1: Dự báo & Phân tích ---
    with tab1:
        input_data = pd.DataFrame({
            'study_hours': [study_hours], 'attendance_rate': [attendance_rate],
            'assignment_completion': [assignment_completion], 'internet_use': [internet_use],
            'motivation': [motivation], 'family_support': [family_support],
            'stress_level': [stress_level], 'part_time_hours': [part_time_hours]
        })

        prediction = model.predict(input_data)
        predicted_score = np.clip(prediction[0], 0, 10)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("🎯 Kết quả dự báo")
            st.metric(label="Điểm Giải tích dự kiến", value=f"{predicted_score:.2f}", delta=f"{predicted_score - df['analytic_score'].mean():.2f} so với trung bình")
            
            st.subheader("💡 Khuyến nghị")
            if predicted_score < 5:
                st.warning("Kết quả học tập cần cải thiện. Hãy tập trung vào các yếu tố có ảnh hưởng tích cực lớn nhất.")
            elif predicted_score < 8:
                st.info("Kết quả khá tốt! Có thể cải thiện thêm bằng cách tối ưu hóa thời gian học và giảm căng thẳng.")
            else:
                st.success("Kết quả rất tốt! Hãy tiếp tục phát huy.")

        with col2:
            st.subheader("📊 Hồ sơ sinh viên")
            categories = list(input_data.columns)
            avg_student = df[categories].mean().values.flatten().tolist()
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=input_data.iloc[0].values, theta=categories, fill='toself', name='Sinh viên hiện tại', line_color='#00A67E'))
            fig.add_trace(go.Scatterpolar(r=avg_student, theta=categories, fill='toself', name='Sinh viên trung bình', line_color='rgba(255, 255, 255, 0.5)'))
            fig.update_layout(
                template="plotly_dark",
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, df[categories].max().max()]),
                    bgcolor='#161A25'
                ),
                paper_bgcolor='#161A25',
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Khám phá Dữ liệu ---
    with tab2:
        st.header("Phân tích Dữ liệu Huấn luyện")
        st.markdown(f"Dữ liệu gồm **{df.shape[0]}** mẫu và **{df.shape[1]-1}** biến đầu vào.")
        
        with st.expander("Xem dữ liệu thô"):
            st.dataframe(df)
        
        with st.expander("Thống kê mô tả"):
            st.dataframe(df.describe())

        st.subheader("Phân phối của các biến")
        selected_col = st.selectbox("Chọn một biến để xem phân phối:", df.columns)
        fig_hist = px.histogram(df, x=selected_col, title=f"Phân phối của {selected_col}", template="plotly_dark")
        st.plotly_chart(fig_hist, use_container_width=True)

        st.subheader("Ma trận tương quan")
        corr_matrix = df.corr()
        fig_heatmap = px.imshow(corr_matrix, text_auto=True, title="Ma trận tương quan giữa các biến", template="plotly_dark")
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- Tab 3: Hiệu suất Mô hình ---
    with tab3:
        st.header("Đánh giá Hiệu suất Mô hình Hồi quy")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("R-squared (R²)", f"{metrics['r2_score']:.4f}")
        col2.metric("Mean Absolute Error (MAE)", f"{metrics['mae']:.4f}")
        col3.metric("Root Mean Squared Error (RMSE)", f"{metrics['rmse']:.4f}")

        st.subheader("Mức độ quan trọng của các yếu tố (Hệ số mô hình)")
        coef = pd.Series(model.coef_, index=df.columns.drop('analytic_score')).sort_values()
        fig_coef = px.bar(coef, x=coef.values, y=coef.index, orientation='h', title="Hệ số của mô hình hồi quy", template="plotly_dark")
        fig_coef.update_layout(xaxis_title="Giá trị hệ số", yaxis_title="Yếu tố", paper_bgcolor='#161A25', plot_bgcolor='#161A25')
        st.plotly_chart(fig_coef, use_container_width=True)
        
        with st.expander("Giải thích hệ số"):
            st.info("""
            - **Hệ số dương:** Yếu tố này có ảnh hưởng tích cực đến điểm số.
            - **Hệ số âm:** Yếu tố này có ảnh hưởng tiêu cực đến điểm số.
            - **Độ lớn:** Cho biết mức độ ảnh hưởng mạnh hay yếu của yếu tố đó.
            """)
