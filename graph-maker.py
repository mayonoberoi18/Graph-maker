import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Beautiful graphs • Smart unit handling • Professional quality**")

# ====================== AXIS UNITS ======================
st.subheader("1. Set Your Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_common = ["Days", "Months", "Time (hours)", "Time (seconds)", "Subjects", 
                "Match No.", "Age (years)", "Distance (km)"]
    x_sug = st.selectbox("Common options", x_common, index=2)
    x_label = st.text_input("Custom X-Axis", value=x_sug, key="x_key")

with col2:
    st.markdown("**Y-Axis Label**")
    y_common = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                "Speed (km/h)", "Weight (kg)", "Runs Scored", "Price (₹)"]
    y_sug = st.selectbox("Common options", y_common, index=2)
    y_label = st.text_input("Custom Y-Axis", value=y_sug, key="y_key")

# Refresh button when units change
if st.button("🔄 Refresh Data with New Units", type="secondary"):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("Data updated with new units!")

# ====================== GRAPH TYPE ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio(
    "Select style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== YOUR DATA SECTION ======================
st.subheader("3. Your Data")

st.markdown("**Load Sample Data**")
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Math", "Science", "English", "History", "Geography", "Hindi"],
            y_label: [85, 92, 78, 65, 88, 82]
        })
        st.rerun()

with c2:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["M1", "M2", "M3", "M4", "M5"],
            y_label: [45, 78, 102, 33, 67]
        })
        st.rerun()

with c3:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y_label: [45000, 52000, 48000, 61000, 55000, 68000]
        })
        st.rerun()

with c4:
    if st.button("📈 Temperature Over Time", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [28, 32, 35, 31, 29, 33]
        })
        st.rerun()

# Data Input
tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Manual Edit"])

with tab1:
    uploaded = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            st.success("✅ File loaded successfully with your units!")
            st.session_state.data = df
            st.rerun()
        except Exception as e:
            st.error(f"Could not read file: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [25, 30, 35, 42, 48, 55]
        })
    
    st.write("**Edit your data:**")
    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited

if 'data' in st.session_state:
    st.subheader("Current Data Preview")
    st.dataframe(st.session_state.data, use_container_width=True)

# ====================== GENERATE GRAPH ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please load sample data or enter your data first.")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Please click 'Refresh Data with New Units' after changing labels.")
            st.stop()

        is_numeric_y = pd.api.types.is_numeric_dtype(df[y_label])

        try:
            title = f"{y_label} vs {x_label}"

            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=title, markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=title)
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=title)
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=title)
            elif "Box" in graph_choice:
                if not is_numeric_y:
                    st.error("Box Plot requires numeric values in Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric_y:
                    st.error("Histogram requires numeric values in Y-axis.")
                    st.stop()
                fig = px.histogram(df, x=y_label, nbins=20, title=f"Distribution of {y_label}")

            # Professional Styling
            fig.update_layout(
                height=720,
                title_font_size=28,
                title_x=0.5,
                font_family="Arial",
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                margin=dict(l=90, r=50, t=100, b=90)
            )

            fig.update_xaxes(
                title_font=dict(size=19, color="#2c3e50"),
                tickfont=dict(size=14),
                gridcolor="rgba(180,180,180,0.4)"
            )
            fig.update_yaxes(
                title_font=dict(size=19, color="#2c3e50"),
                tickfont=dict(size=14),
                gridcolor="rgba(180,180,180,0.4)"
            )

            # Extra polish for Histogram
            if "Histogram" in graph_choice:
                fig.update_traces(
                    marker_color="#3498db",
                    marker_line_color="#2c3e50",
                    marker_line_width=1.2,
                    opacity=0.85
                )

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data (CSV)", csv, "graph_data.csv", "text/csv", use_container_width=True)

            st.success("✅ Professional graph created successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Made with care • Change units freely • Click 'Refresh Data' when needed • Looks professional")
