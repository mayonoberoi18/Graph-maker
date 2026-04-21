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
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Subjects": ["Math", "Science", "English"],
        "Marks": [85, 92, 78]
    })
if 'x_val' not in st.session_state:
    st.session_state.x_val = "Subjects"
if 'y_val' not in st.session_state:
    st.session_state.y_val = "Marks"

# ====================== 1. Axis Labels ======================
st.subheader("1. Set X and Y Axis Labels")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", 
                 "Age (years)", "Distance (km)", "Category"]
    x_index = x_options.index(st.session_state.x_val) if st.session_state.x_val in x_options else 3
    x_label = st.text_input("X label", value=st.session_state.x_val)

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Runs Scored", "Speed (km/h)", "Price", "Count"]
    y_index = y_options.index(st.session_state.y_val) if st.session_state.y_val in y_options else 0
    y_label = st.text_input("Y label", value=st.session_state.y_val)

st.session_state.x_val = x_label
st.session_state.y_val = y_label

if st.button("🔄 Apply New Axis Labels to Data", use_container_width=True):
    old_cols = list(st.session_state.data.columns)
    st.session_state.data = st.session_state.data.rename(columns={
        old_cols[0]: x_label,
        old_cols[1]: y_label
    })
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
        st.session_state.data = pd.DataFrame({"Subjects": ["Math", "Science", "English"], "Marks": [85, 92, 78]})
        st.rerun()
with sample_cols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({"Match No.": ["M1", "M2", "M3"], "Runs Scored": [45, 78, 102]})
        st.rerun()
with sample_cols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({"Months": ["Jan", "Feb", "Mar"], "Sales (₹)": [45000, 52000, 48000]})
        st.rerun()
with sample_cols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.data = pd.DataFrame({"Days": [1, 2, 3], "Temperature (°C)": [28, 32, 35]})
        st.rerun()

# Data Editor
st.subheader("Edit Your Data")
# FIX: The key 'stable_editor' prevents the widget from resetting when adding new rows.
edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="stable_editor"
)
st.session_state.data = edited_df

# ====================== Generate Graph ======================
st.divider()

if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    df = st.session_state.data
    
    if df.empty or len(df.columns) < 2:
        st.error("Please add data with at least two columns.")
        st.stop()
    
    x_col, y_col = df.columns[0], df.columns[1]
    
    # Ensure numeric values for distribution-based plots
    # We attempt to convert to numeric to handle cases where numbers are typed as strings
    df_plot = df.copy()
    df_plot[y_col] = pd.to_numeric(df_plot[y_col], errors='coerce')
    is_numeric_y = not df_plot[y_col].isnull().all()

    try:
        if "Line" in graph_choice:
            fig = px.line(df_plot, x=x_col, y=y_col, markers=True)
        elif "Bar" in graph_choice:
            fig = px.bar(df_plot, x=x_col, y=y_col)
        elif "Scatter" in graph_choice:
            fig = px.scatter(df_plot, x=x_col, y=y_col)
        elif "Area" in graph_choice:
            fig = px.area(df_plot, x=x_col, y=y_col)
        elif "Box" in graph_choice:
            if not is_numeric_y:
                st.error(f"'{y_col}' must be numeric for a Box Plot.")
                st.stop()
            fig = px.box(df_plot, y=y_col)
        elif "Histogram" in graph_choice:
            if not is_numeric_y:
                st.error(f"'{y_col}' must be numeric for a Histogram.")
                st.stop()
            # IMPROVED HISTOGRAM: Connected bars (bargap=0) and continuous look
            fig = px.histogram(df_plot, x=y_col, nbins=10)
            fig.update_layout(bargap=0) # Removes gaps between bars
            fig.update_traces(marker_line_color='white', marker_line_width=0.5)

        fig.update_layout(
            height=600,
            template="plotly_white",
            xaxis_title=st.session_state.x_val,
            yaxis_title="Frequency" if "Histogram" in graph_choice else st.session_state.y_val,
            title=f"{graph_choice.split()[-1]} of {st.session_state.y_val}"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

st.caption("Made with ❤️ by Mayon Oberoi")
