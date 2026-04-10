import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cấu hình trang với layout wide và tiêu đề
st.set_page_config(
    page_title="Financial Dashboard | BIDV",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS để giao diện trông cao cấp hơn
st.markdown("""
<style>
    /* Gradient Background for header */
    .block-container {
        padding-top: 2rem !important;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #007A5A, #FFC20E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }
    /* Style cho metric cards tự build */
    .custom-metric {
        background-color: #ffffff;
        border: 1px solid #dce4f0;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border-left: 5px solid #007A5A;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .custom-metric:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #007A5A;
        line-height: 1.1;
    }
    .metric-unit {
        font-size: 0.9rem;
        color: #888;
        font-weight: 500;
        margin-top: 4px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("BID.xlsx")
        # Đảm bảo cột Năm là kiểu số (nếu có null thì drop)
        df = df.dropna(subset=['Năm']).copy()
        df['Năm'] = df['Năm'].astype(int)
        df = df.sort_values(by='Năm', ascending=True)
        return df
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        return pd.DataFrame()

df = load_data()

st.title("Dashboard Phân tích dữ liệu tài chính vĩ mô – BIDV")
st.image("https://bidv.com.vn/wps/wcm/connect/91818b83-ec61-4ab4-9367-b196d446d60c/d838501beb8947d71e98.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-91818b83-ec61-4ab4-9367-b196d446d60c-oWnmrwW", use_container_width=True)
st.markdown("*Nền tảng trực quan hóa thông số tài chính chuyên sâu và tự động.*")

if df.empty:
    st.warning("Không có dữ liệu trong file BID.xlsx")
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.header("Bộ lọc Dữ Liệu")

min_year = int(df['Năm'].min())
max_year = int(df['Năm'].max())
selected_years = st.sidebar.slider("Chọn Giai Đoạn", min_year, max_year, (min_year, max_year))

# Lọc dữ liệu theo năm
filtered_df = df[(df['Năm'] >= selected_years[0]) & (df['Năm'] <= selected_years[1])]

st.sidebar.markdown("---")
st.sidebar.info(
    "**Thông tin:**\n"
    "Dashboard sử dụng dữ liệu trích xuất từ file báo cáo tài chính nội bộ. "
    "Mô hình đang trực quan hóa sức khỏe tài chính thông qua dòng tiền và tài sản."
)

# --- KPIs SECTION ---
st.markdown("### Chỉ số Tài Chính Nổi Bật (Năm Gần Nhất)")

# Lấy dữ liệu của năm mới nhất trong khoảng thời gian đã chọn
latest_year = filtered_df['Năm'].max()
latest_data = filtered_df[filtered_df['Năm'] == latest_year].iloc[0] if not filtered_df.empty else None

if latest_data is not None:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tong_tai_san = latest_data.get('TỔNG CỘNG TÀI SẢN (đồng)', 0) / 1e12
        st.markdown(f'<div class="custom-metric"><div class="metric-label">Tổng Tài Sản ({latest_year})</div><div class="metric-value">{tong_tai_san:,.1f}</div><div class="metric-unit">Nghìn Tỷ VNĐ</div></div>', unsafe_allow_html=True)
    with col2:
        von_chu = latest_data.get('VỐN CHỦ SỞ HỮU (đồng)', 0) / 1e12
        st.markdown(f'<div class="custom-metric"><div class="metric-label">Vốn Chủ Sở Hữu ({latest_year})</div><div class="metric-value">{von_chu:,.1f}</div><div class="metric-unit">Nghìn Tỷ VNĐ</div></div>', unsafe_allow_html=True)
    with col3:
        cho_vay = latest_data.get('Cho vay khách hàng', 0) / 1e12
        st.markdown(f'<div class="custom-metric"><div class="metric-label">Dư Nợ Cho Vay ({latest_year})</div><div class="metric-value">{cho_vay:,.1f}</div><div class="metric-unit">Nghìn Tỷ VNĐ</div></div>', unsafe_allow_html=True)
    with col4:
        tien_gui = latest_data.get('Tiền gửi của khách hàng', 0) / 1e12
        st.markdown(f'<div class="custom-metric"><div class="metric-label">Tiền Gửi Khách Hàng ({latest_year})</div><div class="metric-value">{tien_gui:,.1f}</div><div class="metric-unit">Nghìn Tỷ VNĐ</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- CHARTS SECTION ---

# Định luật màu sắc thống nhất (Palette)
custom_palette = px.colors.qualitative.Prism

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Tăng trưởng tài sản và Vốn chủ sở hữu")
    # Vẽ biểu đồ Line với 2 trục y khác nhau hoặc chung nếu scaling tương tự
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df['Năm'], 
        y=filtered_df['TỔNG CỘNG TÀI SẢN (đồng)'] / 1e12,
        mode='lines+markers',
        name='Tổng Tài Sản',
        line=dict(color='#007A5A', width=3),
        marker=dict(size=8, symbol='square')
    ))
    fig1.add_trace(go.Bar(
        x=filtered_df['Năm'], 
        y=filtered_df['VỐN CHỦ SỞ HỮU (đồng)'] / 1e12,
        name='Vốn Chủ Sở Hữu',
        marker_color='#FFC20E',
        opacity=0.8
    ))
    fig1.update_layout(
        height=450,
        xaxis_title='Năm',
        yaxis_title='Giá trị (Nghìn Tỷ VNĐ)',
        hovermode="x unified",
        template="simple_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="rgba(0, 122, 90, 0.2)", font_size=14, font_color="#004D40")
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("💼 Cho vay và Huy động khách hàng")
    fig2 = go.Figure(data=[
        go.Bar(name='Cho Vay Khách Hàng', x=filtered_df['Năm'], y=filtered_df['Cho vay khách hàng']/1e12, marker_color='#007A5A'),
        go.Bar(name='Tiền Gửi Khách Hàng', x=filtered_df['Năm'], y=filtered_df['Tiền gửi của khách hàng']/1e12, marker_color='#FFC20E')
    ])
    fig2.update_layout(
        height=450,
        barmode='group',
        xaxis_title='Năm',
        yaxis_title='Giá trị (Nghìn Tỷ VNĐ)',
        hovermode="x unified",
        template="simple_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="rgba(0, 122, 90, 0.2)", font_size=14, font_color="#004D40")
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col_line, col_pie = st.columns(2)

with col_line:
    st.subheader("📊 Mật độ tiền gửi và chứng khoán đầu tư")
    line_df = filtered_df[['Năm', 'Tiền và tương đương tiền (đồng)', 'Chứng khoán đầu tư', 'Chứng khoán kinh doanh']].copy()
    line_df.set_index('Năm', inplace=True)
    line_df = line_df / 1e12 # Quy đổi về ngàn tỷ
    fig3 = px.area(line_df, x=line_df.index, y=line_df.columns, 
                   color_discrete_sequence=['#007A5A', '#FFC20E', '#4CA18A'],
                   labels={"value": "Nghìn Tỷ VNĐ", "variable": "Danh mục"})
    fig3.update_layout(
        height=450, 
        hovermode="x unified",
        template="simple_white", 
        legend_title_text="Loại Tài Sản",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hoverlabel=dict(bgcolor="rgba(0, 122, 90, 0.2)", font_size=14, font_color="#004D40")
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_pie:
    st.subheader("Cơ cấu nguồn vốn mới nhất")
    if latest_data is not None:
        von_chu = latest_data.get('VỐN CHỦ SỞ HỮU (đồng)', 0)
        no_phai_tra = latest_data.get('NỢ PHẢI TRẢ (đồng)', 0)
        labels = ['Vốn Chủ Sở Hữu', 'Nợ Phải Trả']
        values = [von_chu, no_phai_tra]
        fig4 = px.pie(names=labels, values=values, hole=0.5,
                      color_discrete_sequence=['#007A5A', '#FFC20E'])
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        fig4.update_layout(
            height=450, 
            showlegend=False, 
            template="simple_white",
            hoverlabel=dict(bgcolor="rgba(0, 122, 90, 0.2)", font_size=14, font_color="#004D40")
        )
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("© 2026 Financial Data Analytics System. Built with Streamlit & Plotly.")
