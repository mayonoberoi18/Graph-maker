import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Graph Maker")
st.markdown("**Change Units • Edit Data • Make Graphs• By Mayon Oberoi • Illuminati**")

# --- Logic to handle title updates ---
if 'x_val' not in st.session_state:
    st.session_state.x_val = "Subjects"
if 'y_val' not in st.session_state:
    st.session_state.y_val = "Marks"

# ====================== 1. Units ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", "Age (years)", "Distance (km)"]
    try:
        x_index = x_options.index(st.session_state.x_val)
    except ValueError:
        x_index = 3
    
    x_sug = st.selectbox("Common X units", x_options, index=x_index)
    x_label = st.text_input("Or type custom", value=st.session_state.x_val, key="x_input_box")
    st.session_state.x_val = x_label 

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", "Runs Scored", "Speed (km/h)"]
    try:
        y_index = y_options.index(st.session_state.y_val)
    except ValueError:
        y_index = 0
        
    y_sug = st.selectbox("Common Y units", y_options, index=y_index)
    y_label = st.text_input("Or type custom", value=st.session_state.y_val, key="y_input_box")
    st.session_state.y_val = y_label

if st.button("🔄 Refresh Data with New Units", use_container_width=True):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("Units updated successfully!")

# ====================== 2. File Upload ======================
st.subheader("2. Upload Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read Excel
        df_upload = pd.read_excel(uploaded_file)
        if len(df_upload.columns) >= 2:
            # Automatically update titles/units based on file columns
            st.session_state.x_val = str(df_upload.columns[0])
            st.session_state.y_val = str(df_upload.columns[1])
            st.session_state.data = df_upload.iloc[:, :2] # Take first two columns
            st.success("File Loaded Successfully!")
        else:
            st.error("Excel file must have at least 2 columns.")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.error("File is not loaded")

# ====================== 3. Graph Type ======================
st.subheader("3. Choose Graph Type")
graph_choice = st.radio("Select style", 
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True)

# ====================== 4. Data Input ======================
st.subheader("4. Add / Edit Your Data")

st.markdown("**Sample Data**")
scols = st.columns(4)
with scols[0]:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.x_val = "Subjects"
        st.session_state.y_val = "Marks"
        st.session_state.data = pd.DataFrame({"Subjects": ["Math","Science","English","History","Geo","Hindi"], "Marks": [85,92,78,65,88,82]})
        st.rerun()
with scols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.x_val = "Match No."
        st.session_state.y_val = "Runs Scored"
        st.session_state.data = pd.DataFrame({"Match No.": ["M1","M2","M3","M4","M5"], "Runs Scored": [45,78,102,33,67]})
        st.rerun()
with scols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.x_val = "Months"
        st.session_state.y_val = "Sales (₹)"
        st.session_state.data = pd.DataFrame({"Months": ["Jan","Feb","Mar","Apr","May","Jun"], "Sales (₹)": [45000,52000,48000,61000,55000,68000]})
        st.rerun()
with scols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.x_val = "Days"
        st.session_state.y_val = "Temperature (°C)"
        st.session_state.data = pd.DataFrame({"Days": [1,2,3,4,5,6], "Temperature (°C)": [28,32,35,31,29,33]})
        st.rerun()

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({st.session_state.x_val: ["Math", "Science", "English"], st.session_state.y_val: [85, 92, 78]})

st.subheader("Edit Your Data")
edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key=f"editor_{st.session_state.x_val}_{st.session_state.y_val}"
)
st.session_state.data = edited_df

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please upload file or load sample data")
    else:
        df = st.session_state.data.copy()
        
        # Using state values for consistency
        current_x = st.session_state.x_val
        current_y = st.session_state.y_val

        try:
            if "Line" in graph_choice:
                fig = px.line(df, x=current_x, y=current_y, title=f"{current_y} vs {current_x
