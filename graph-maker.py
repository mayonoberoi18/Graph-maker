import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**The complete & smooth version** — Upload Excel • Make your own graph • Change units easily")

# ====================== SESSION STATE ======================
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "X": [1, 2, 3, 4, 5, 6, 7, 8],
        "Y": [10, 25, 35, 48, 62, 75, 80, 95]
    })
if 'x_label' not in st.session_state:
    st.session_state.x_label = "Time (hours)"
if 'y_label' not in st.session_state:
    st.session_state.y_label = "Temperature (°C)"

# ====================== 1. AXIS UNITS ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Time (seconds)", "Subjects", 
                 "Match No.", "Age (years)", "Distance (km)"]
    x_sug = st.selectbox("Common X units", x_options, index=2, key="x_sug")
    x_label = st.text_input("Custom X label", value=x_sug, key="x_custom")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Speed (km/h)", "Weight (kg)", "Runs Scored", "Price (₹)"]
    y_sug = st.selectbox("Common Y units", y_options, index=2, key="y_sug")
    y_label = st.text_input("Custom Y label", value=y_sug, key="y_custom")

# Update session state
st.session_state.x_label = x_label
st.session_state.y_label = y_label

if st.button("🔄 Refresh Data with New Units", type="secondary", use_container_width=True):
    st.success("✅ Units updated! Edit data if needed and click Generate Graph.")
    # Rename columns in existing data
    if 'data' in st.session_state and len(st.session_state.data.columns) >= 2:
        st.session_state.data.columns = [x_label, y_label]

# ====================== 2. GRAPH TYPE ======================
st.subheader("2. Choose Graph Type")
graph_type = st.radio(
    "Select style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== 3. DATA ======================
st.subheader("3. Your Data")

tab1, tab2 = st.tabs(["✏️ Manual Entry (Make Your Own)", "📁 Upload Excel / CSV"])

with tab1:
    st.info("Type or edit your data here. You can change text and numbers freely.")
    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="manual_editor"
    )
    st.session_state.data = edited

with tab2:
    st.info("Upload your file (your CSV files will work)")
    uploaded = st.file_uploader("Choose file", type=["csv", "xlsx", "xls"])
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded, engine='openpyxl')
            
            st.success(f"✅ File loaded: {uploaded.name}")
            st.write("**Columns found:**", list(df.columns))
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
                st.success("Using first two columns with your current labels")
            
            st.session_state.data = df
            st.rerun()
        except Exception as e:
            st.error(f"Could not read file: {e}")

# Data Preview
st.subheader("Current Data")
st.dataframe(st.session_state.data, use_container_width=True)

# ====================== GENERATE GRAPH ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    df = st.session_state.data.copy()
    df = df.dropna(how='all')  # remove empty rows
    
    if len(df) < 1:
        st.error("Please add some data in the table above.")
        st.stop()

    # Ensure column names are correct
    df.columns = [x_label, y_label]

    y_numeric = pd.api.types.is_numeric_dtype(df[y_label])

    try:
        title = f"{y_label} vs {x_label}"

        if graph_type == "Line Chart":
            fig = px.line(df, x=x_label, y=y_label, title=title, markers=True)
        elif graph_type == "Bar Chart":
            fig = px.bar(df, x=x_label, y=y_label, title=title)
        elif graph_type == "Scatter Plot":
            fig = px.scatter(df, x=x_label, y=y_label, title=title)
        elif graph_type == "Area Chart":
            fig = px.area(df, x=x_label, y=y_label, title=title)
        elif graph_type == "Box Plot":
            if not y_numeric:
                st.error("Box Plot and Histogram need numbers in Y column.")
                st.stop()
            fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
        elif graph_type == "Histogram":
            if not y_numeric:
                st.error("Box Plot and Histogram need numbers in Y column.")
                st.stop()
            fig = px.histogram(df, x=y_label, nbins=25, title=f"Distribution of {y_label}", opacity=0.85)
            fig.update_traces(marker_color="#1f77b4", marker_line_color="black", marker_line_width=1.5)

        # Professional styling
        fig.update_layout(
            height=720,
            title_font_size=28,
            title_x=0.5,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white",
            margin=dict(l=80, r=50, t=100, b=80)
        )
        fig.update_xaxes(title_font=dict(size=18), tickfont=dict(size=14))
        fig.update_yaxes(title_font=dict(size=18), tickfont=dict(size=14))

        st.plotly_chart(fig, use_container_width=True)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data as CSV", csv, "my_graph_data.csv", "text/csv", use_container_width=True)

        st.success("✅ Graph generated successfully!")

    except Exception as e:
        st.error(f"Error generating graph: {e}")
        st.info("Tip: Make sure Y column has only numbers for Box Plot and Histogram.")

st.caption("How to use: Set labels → Click Refresh button → Edit data → Choose graph type → Generate Graph")
