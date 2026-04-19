import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Graph Maker")
st.markdown("**Professional graphs with easy editing, by Mayon Oberoi.Illuminati**")

# ====================== Units ======================
st.subheader("1. Set Your Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_common = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", "Age (years)"]
    x_sug = st.selectbox("Common X options", x_common, index=3)   # Subjects as default
    x_label = st.text_input("Custom X-Axis", value=x_sug, key="x_key")

with col2:
    st.markdown("**Y-Axis Label**")
    y_common = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", "Runs Scored"]
    y_sug = st.selectbox("Common Y options", y_common, index=0)
    y_label = st.text_input("Custom Y-Axis", value=y_sug, key="y_key")

if st.button("🔄 Refresh Data with New Units", type="secondary"):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("✅ Units updated!")

# ====================== Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio(
    "Select style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== Your Data ======================
st.subheader("3. Your Data")

st.markdown("**Load Sample Data**")
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Math", "Science", "English", "History", "Geography", "Hindi"],
            y_label: [85, 92, 78, 65, 88, 82]
        })
        st.success("Loaded! Now edit names and numbers below.")
        st.rerun()

with c2:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: ["M1","M2","M3","M4","M5"], y_label: [45,78,102,33,67]})
        st.rerun()

with c3:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: ["Jan","Feb","Mar","Apr","May","Jun"], y_label: [45000,52000,48000,61000,55000,68000]})
        st.rerun()

with c4:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: [1,2,3,4,5,6], y_label: [28,32,35,31,29,33]})
        st.rerun()

tab1, tab2 = st.tabs(["📁 Upload Excel/CSV", "✏️ Edit Data"])

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
            st.success("✅ File loaded!")
            st.session_state.data = df
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: ["Item 1", "Item 2", "Item 3", "Item 4"],
            y_label: [45, 67, 82, 55]
        })
    
    st.write("**Edit names and numbers freely here:**")
    st.info("→ You can change subject names in X column and numbers in Y column")
    
    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            x_label: st.column_config.TextColumn("X-Axis (e.g. Subjects)"),
            y_label: st.column_config.NumberColumn("Y-Axis (Numbers only)", format="%d")
        }
    )
    st.session_state.data = edited

if 'data' in st.session_state:
    st.subheader("Current Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please load or edit data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Click 'Refresh Data with New Units' after changing labels.")
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
                    st.error("Box Plot needs numbers in Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric_y:
                    st.error("Histogram needs numbers in Y-axis.")
                    st.stop()
                fig = px.histogram(df, x=y_label, nbins=20, title=f"Distribution of {y_label}", opacity=0.85)
                fig.update_traces(marker_color="#3498db", marker_line_color="#2c3e50", marker_line_width=1.5)

            # Professional Look
            fig.update_layout(
                height=720,
                title_font_size=28,
                title_x=0.5,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                margin=dict(l=90, r=50, t=110, b=90)
            )

            fig.update_xaxes(title_font=dict(size=19), tickfont=dict(size=14))
            fig.update_yaxes(title_font=dict(size=19), tickfont=dict(size=14))

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "graph_data.csv", "text/csv", use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("You can also download the data.")
