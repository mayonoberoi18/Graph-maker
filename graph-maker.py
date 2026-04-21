import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Graph Maker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Graph Maker")
st.markdown("**Change Units • Edit Data • Make Graphs** \n*By Mayon Oberoi • Illuminati*")

# ====================== Session State Initialization ======================
if 'x_val' not in st.session_state:
    st.session_state.x_val = "Subjects"
if 'y_val' not in st.session_state:
    st.session_state.y_val = "Marks"
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Subjects": ["Math", "Science", "English"],
        "Marks": [85, 92, 78]
    })

# ====================== 1. Axis Labels ======================
st.subheader("1. Set X and Y Axis Labels")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", 
                 "Age (years)", "Distance (km)", "Category"]
    x_index = x_options.index(st.session_state.x_val) if st.session_state.x_val in x_options else 3
    
    x_sug = st.selectbox("Common X labels", x_options, index=x_index, key="x_sug")
    x_label = st.text_input("Or type custom X label", value=st.session_state.x_val, key="x_input")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Runs Scored", "Speed (km/h)", "Price", "Count"]
    y_index = y_options.index(st.session_state.y_val) if st.session_state.y_val in y_options else 0
    
    y_sug = st.selectbox("Common Y labels", y_options, index=y_index, key="y_sug")
    y_label = st.text_input("Or type custom Y label", value=st.session_state.y_val, key="y_input")

# Update session state
if x_label != st.session_state.x_val or y_label != st.session_state.y_val:
    st.session_state.x_val = x_label
    st.session_state.y_val = y_label

# Refresh button to rename columns
if st.button("🔄 Apply New Axis Labels to Data", use_container_width=True, type="secondary"):
    if 'data' in st.session_state and not st.session_state.data.empty:
        old_cols = list(st.session_state.data.columns)
        if len(old_cols) >= 2:
            st.session_state.data = st.session_state.data.rename(columns={
                old_cols[0]: x_label,
                old_cols[1]: y_label
            })
            st.success(f"Columns updated to: **{x_label}** and **{y_label}**")
            st.rerun()

# ====================== 2. Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio(
    "Select graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True,
    label_visibility="collapsed"
)

# ====================== 3. Sample Data & Editor ======================
st.subheader("3. Load Sample Data or Edit Manually")

sample_cols = st.columns(4)

with sample_cols[0]:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.x_val = "Subjects"
        st.session_state.y_val = "Marks"
        st.session_state.data = pd.DataFrame({
            "Subjects": ["Math", "Science", "English", "History", "Geography", "Hindi"],
            "Marks": [85, 92, 78, 65, 88, 82]
        })
        st.rerun()

with sample_cols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.x_val = "Match No."
        st.session_state.y_val = "Runs Scored"
        st.session_state.data = pd.DataFrame({
            "Match No.": ["M1", "M2", "M3", "M4", "M5"],
            "Runs Scored": [45, 78, 102, 33, 67]
        })
        st.rerun()

with sample_cols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.x_val = "Months"
        st.session_state.y_val = "Sales (₹)"
        st.session_state.data = pd.DataFrame({
            "Months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Sales (₹)": [45000, 52000, 48000, 61000, 55000, 68000]
        })
        st.rerun()

with sample_cols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.x_val = "Days"
        st.session_state.y_val = "Temperature (°C)"
        st.session_state.data = pd.DataFrame({
            "Days": [1, 2, 3, 4, 5, 6],
            "Temperature (°C)": [28, 32, 35, 31, 29, 33]
        })
        st.rerun()

# Data Editor
st.subheader("Edit Your Data")
st.info("👈 Edit values directly below. Add/remove rows as needed.")

# FIX: Changed key to a static string 'main_data_editor' to stop the "first-try" bug
edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="main_data_editor"
)

st.session_state.data = edited_df

# Data Preview
if not st.session_state.data.empty:
    st.subheader("Current Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# ====================== Generate Graph ======================
st.divider()

if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    df = st.session_state.data.copy()
    
    if df.empty:
        st.error("Please add some data first!")
        st.stop()
    
    current_cols = list(df.columns)
    if len(current_cols) < 2:
        st.error("Data must have at least 2 columns")
        st.stop()
    
    x_col = current_cols[0]
    y_col = current_cols[1]
    
    try:
        is_numeric_y = pd.api.types.is_numeric_dtype(df[y_col])
        
        if "Line" in graph_choice:
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}", markers=True)
        elif "Bar" in graph_choice:
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        elif "Scatter" in graph_choice:
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        elif "Area" in graph_choice:
            fig = px.area(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        elif "Box" in graph_choice:
            if not is_numeric_y:
                st.error("Box Plot requires numeric values in Y column")
                st.stop()
            fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
        elif "Histogram" in graph_choice:
            if not is_numeric_y:
                st.error("Histogram requires numeric values in Y column")
                st.stop()
            fig = px.histogram(df, x=y_col, nbins=20, title=f"Distribution of {y_col}")
            fig.update_traces(marker_color="#1f77b4", marker_line_color="black", marker_line_width=1)
        
        # Layout improvements
        fig.update_layout(
            height=650,
            title_font_size=28,
            title_x=0.5,
            template="plotly_white",
            xaxis_title=x_label,
            yaxis_title=y_label,
            margin=dict(t=80, b=60)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Data as CSV",
            data=csv,
            file_name="graph_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error generating graph: {e}")

st.caption("Made with ❤️ by Mayon Oberoi")
