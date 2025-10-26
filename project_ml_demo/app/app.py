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

# --- CSS Tùy chỉnh với nhiều màu sắc, animation và responsive ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
        color: #FAFAFA;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid rgba(0, 255, 255, 0.3);
        box-shadow: 4px 0 20px rgba(0, 255, 255, 0.1);
    }
    
    .main .block-container {
        animation: fadeIn 1s ease-out;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1 {
        background: linear-gradient(90deg, #00F5FF 0%, #00D4FF 25%, #00B4FF 50%, #0094FF 75%, #00F5FF 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s linear infinite;
        font-weight: 700;
    }
    
    h2 {
        color: #00F5FF;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
    }
    
    h3 {
        color: #00D4FF;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 148, 255, 0.1) 100%);
        border: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.4);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #FFFFFF;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }
    
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 245, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #FFFFFF;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(0, 148, 255, 0.2) 100%);
        border: 2px solid #00F5FF;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
    }
    
    @media (max-width: 768px) {
        .main .block-container { padding-left: 1rem; padding-right: 1rem; }
        h1 { font-size: 1.8rem; }
        h2 { font-size: 1.4rem; }
        .stButton>button { font-size: 0.9rem; padding: 10px 16px; }
    }
    
    @media (max-width: 480px) {
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.2rem; }
    }
    
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# --- Các hàm tải tài nguyên ---
@st.cache_resource
def load_model():
    """Tải mô hình hồi quy."""
    # Hỗ trợ cả đường dẫn tương đối và tuyệt đối
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '../model', 'regression_model.pkl')
    
    # Nếu không tìm thấy, thử đường dẫn khác
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(current_dir), 'model', 'regression_model.pkl')
    
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

@st.cache_data
def load_data():
    """Tải dữ liệu huấn luyện."""
    # Hỗ trợ cả đường dẫn tương đối và tuyệt đối
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../data', 'synthetic_data.csv')
    
    # Nếu không tìm thấy, thử đường dẫn khác
    if not os.path.exists(data_path):
        data_path = os.path.join(os.path.dirname(current_dir), 'data', 'synthetic_data.csv')
    
    if not os.path.exists(data_path):
        return None
    return pd.read_csv(data_path)

@st.cache_data
def load_metrics():
    """Tải các chỉ số đánh giá mô hình."""
    # Hỗ trợ cả đường dẫn tương đối và tuyệt đối
    current_dir = os.path.dirname(os.path.abspath(__file__))
    metrics_path = os.path.join(current_dir, '../model', 'model_metrics.json')
    
    # Nếu không tìm thấy, thử đường dẫn khác
    if not os.path.exists(metrics_path):
        metrics_path = os.path.join(os.path.dirname(current_dir), 'model', 'model_metrics.json')
    
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
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>🎓</h1>
        <h2 style='margin: 0.5rem 0; color: #00F5FF;'>Dashboard Dự báo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%); 
                padding: 1rem; border-radius: 10px; border: 1px solid rgba(0, 245, 255, 0.3); 
                margin-bottom: 1rem; text-align: center;'>
        <p style='margin: 0; color: #FAFAFA; font-size: 0.95rem;'>✨ Điều chỉnh các thông số đầu vào để dự báo điểm môn Giải tích của sinh viên ✨</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.markdown("<h3 style='text-align: center; color: #00F5FF;'>📝 Thông số đầu vào</h3>", unsafe_allow_html=True)
        
        st.markdown("##### 📚 Học tập")
        study_hours = st.slider("⏰ Giờ tự học/tuần", 0.0, 20.0, 10.0, 0.5)
        attendance_rate = st.slider("✅ Tỷ lệ chuyên cần (%)", 50.0, 100.0, 85.0)
        assignment_completion = st.slider("📋 Tỷ lệ hoàn thành BT (%)", 50.0, 100.0, 90.0)
        internet_use = st.slider("💻 Giờ học online/tuần", 0.0, 10.0, 5.0, 0.5)
        
        st.markdown("##### 🎯 Yếu tố cá nhân")
        motivation = st.select_slider("🔥 Động lực học tập", [1, 2, 3, 4, 5], 3)
        family_support = st.select_slider("👨‍👩‍👧 Hỗ trợ từ gia đình", [1, 2, 3, 4, 5], 4)
        stress_level = st.select_slider("😰 Mức độ căng thẳng", [1, 2, 3, 4, 5], 2)
        part_time_hours = st.slider("💼 Giờ làm thêm/tuần", 0.0, 20.0, 5.0, 0.5)
        
        submit_button = st.form_submit_button(label="🚀 DỰ ĐOÁN NGAY")

# --- Giao diện chính ---
if model is None or df is None or metrics is None:
    st.error("⚠️ Lỗi: Không tìm thấy mô hình, dữ liệu hoặc chỉ số. Vui lòng chạy `python app/utils.py` để tạo chúng.")
else:
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>📊 Dashboard Phân tích và Dự báo Điểm 🎯</h1>
        <p style='font-size: 1.2rem; color: #00D4FF; margin: 0;'>✨ Chào mừng bạn đến với dashboard tương tác ✨</p>
        <p style='color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem;'>Sử dụng thanh bên trái để nhập dữ liệu và xem kết quả dự báo chi tiết</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='height: 3px; background: linear-gradient(90deg, transparent, #00F5FF, #667eea, #764ba2, transparent); 
                margin: 1rem 0 2rem 0; border-radius: 2px;'></div>
    """, unsafe_allow_html=True)

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
            st.markdown("<h2 style='text-align: center;'>🎯 Kết quả dự báo</h2>", unsafe_allow_html=True)
            
            # Score display with visual indicator
            score_color = "#4CAF50" if predicted_score >= 8 else "#FFC107" if predicted_score >= 5 else "#FF5252"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(0, 245, 255, 0.15) 0%, rgba(102, 126, 234, 0.15) 100%);
                        padding: 2rem; border-radius: 15px; text-align: center; 
                        border: 2px solid rgba(0, 245, 255, 0.4); margin: 1rem 0;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);'>
                <p style='color: rgba(255, 255, 255, 0.8); font-size: 1rem; margin: 0;'>Điểm Giải tích dự kiến</p>
                <h1 style='color: {score_color}; font-size: 4rem; margin: 1rem 0; 
                           text-shadow: 0 0 30px {score_color};'>{predicted_score:.2f}</h1>
                <div style='background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, {score_color}, {score_color}80); 
                                width: {predicted_score * 10}%; height: 100%; transition: width 1s ease;'></div>
                </div>
                <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 1rem;'>
                    {predicted_score - df['analytic_score'].mean():+.2f} so với trung bình
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='text-align: center; margin-top: 2rem;'>💡 Khuyến nghị</h3>", unsafe_allow_html=True)
            if predicted_score < 5:
                st.warning("⚠️ **Cần cải thiện:** Kết quả học tập cần cải thiện. Hãy tập trung vào các yếu tố có ảnh hưởng tích cực lớn nhất.")
            elif predicted_score < 8:
                st.info("📈 **Khá tốt:** Kết quả khá tốt! Có thể cải thiện thêm bằng cách tối ưu hóa thời gian học và giảm căng thẳng.")
            else:
                st.success("🌟 **Xuất sắc:** Kết quả rất tốt! Hãy tiếp tục phát huy.")

        with col2:
            st.markdown("<h2 style='text-align: center;'>📊 Hồ sơ sinh viên</h2>", unsafe_allow_html=True)
            categories = list(input_data.columns)
            avg_student = df[categories].mean().values.flatten().tolist()
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=input_data.iloc[0].values, 
                theta=categories, 
                fill='toself', 
                name='Sinh viên hiện tại', 
                line=dict(color='#00F5FF', width=3),
                fillcolor='rgba(0, 245, 255, 0.3)'
            ))
            fig.add_trace(go.Scatterpolar(
                r=avg_student, 
                theta=categories, 
                fill='toself', 
                name='Sinh viên trung bình', 
                line=dict(color='#FFC107', width=2),
                fillcolor='rgba(255, 193, 7, 0.2)'
            ))
            fig.update_layout(
                template="plotly_dark",
                polar=dict(
                    radialaxis=dict(
                        visible=True, 
                        range=[0, df[categories].max().max()],
                        gridcolor='rgba(255, 255, 255, 0.2)'
                    ),
                    bgcolor='rgba(0, 0, 0, 0.3)',
                    angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)')
                ),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(0, 0, 0, 0.5)',
                    bordercolor='rgba(0, 245, 255, 0.3)',
                    borderwidth=1
                ),
                font=dict(color='#FAFAFA', size=12)
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Khám phá Dữ liệu ---
    with tab2:
        st.markdown("<h2 style='text-align: center;'>📊 Phân tích Dữ liệu Huấn luyện</h2>", unsafe_allow_html=True)
        
        # Stats cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Tổng mẫu", f"{df.shape[0]}")
        with col2:
            st.metric("📊 Biến đầu vào", f"{df.shape[1]-1}")
        with col3:
            st.metric("📈 Điểm TB", f"{df['analytic_score'].mean():.2f}")
        with col4:
            st.metric("🎯 Điểm cao nhất", f"{df['analytic_score'].max():.2f}")
        
        with st.expander("🔍 Xem dữ liệu thô"):
            st.dataframe(df, use_container_width=True)
        
        with st.expander("📈 Thống kê mô tả"):
            st.dataframe(df.describe(), use_container_width=True)

        st.markdown("<h3 style='margin-top: 2rem;'>📊 Phân phối của các biến</h3>", unsafe_allow_html=True)
        selected_col = st.selectbox("Chọn một biến để xem phân phối:", df.columns)
        fig_hist = px.histogram(
            df, 
            x=selected_col, 
            title=f"Phân phối của {selected_col}", 
            template="plotly_dark",
            color_discrete_sequence=['#00F5FF']
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0.3)',
            font=dict(color='#FAFAFA')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("<h3 style='margin-top: 2rem;'>🔥 Ma trận tương quan</h3>", unsafe_allow_html=True)
        corr_matrix = df.corr()
        fig_heatmap = px.imshow(
            corr_matrix, 
            text_auto='.2f', 
            title="Ma trận tương quan giữa các biến", 
            template="plotly_dark",
            color_continuous_scale='RdBu_r'
        )
        fig_heatmap.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#FAFAFA')
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- Tab 3: Hiệu suất Mô hình ---
    with tab3:
        st.markdown("<h2 style='text-align: center;'>⚙️ Đánh giá Hiệu suất Mô hình Hồi quy</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 R-squared (R²)", f"{metrics['r2_score']:.4f}", help="Hệ số xác định - đo lường mức độ phù hợp của mô hình")
        col2.metric("📉 Mean Absolute Error", f"{metrics['mae']:.4f}", help="Sai số tuyệt đối trung bình")
        col3.metric("📈 Root Mean Squared Error", f"{metrics['rmse']:.4f}", help="Căn bậc hai của sai số bình phương trung bình")

        st.markdown("<h3 style='margin-top: 2rem; text-align: center;'>🎯 Mức độ quan trọng của các yếu tố</h3>", unsafe_allow_html=True)
        coef = pd.Series(model.coef_, index=df.columns.drop('analytic_score')).sort_values()
        
        # Color code based on positive/negative
        colors = ['#FF5252' if x < 0 else '#4CAF50' for x in coef.values]
        
        fig_coef = go.Figure(go.Bar(
            x=coef.values,
            y=coef.index,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
            ),
            text=[f"{x:.3f}" for x in coef.values],
            textposition='auto',
        ))
        fig_coef.update_layout(
            title="Hệ số của mô hình hồi quy",
            xaxis_title="Giá trị hệ số",
            yaxis_title="Yếu tố",
            template="plotly_dark",
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0.3)',
            font=dict(color='#FAFAFA', size=12),
            showlegend=False
        )
        st.plotly_chart(fig_coef, use_container_width=True)
        
        with st.expander("ℹ️ Giải thích hệ số"):
            st.markdown("""
            <div style='background: rgba(0, 245, 255, 0.1); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(0, 245, 255, 0.3);'>
                <p style='margin: 0.5rem 0;'><span style='color: #4CAF50; font-weight: bold;'>● Hệ số dương (màu xanh):</span> Yếu tố này có ảnh hưởng tích cực đến điểm số.</p>
                <p style='margin: 0.5rem 0;'><span style='color: #FF5252; font-weight: bold;'>● Hệ số âm (màu đỏ):</span> Yếu tố này có ảnh hưởng tiêu cực đến điểm số.</p>
                <p style='margin: 0.5rem 0;'><span style='color: #00F5FF; font-weight: bold;'>● Độ lớn:</span> Cho biết mức độ ảnh hưởng mạnh hay yếu của yếu tố đó.</p>
            </div>
            """, unsafe_allow_html=True)
