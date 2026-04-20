import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Graph Maker")
st.markdown("**Change Units • Edit Data • Make Graphs• By Mayon Oberoi • Illuminati**")

# Initialize session state for labels if not present
if 'x_label_val' not in st.session_state:
    st.session_state.x_label_val = "Subjects"
if 'y_label_val' not in st.session_state:
    st.session_state.y_label_val = "Marks"

# ====================== 1. Units ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", "Age (years)", "Distance (km)"]
    try:
        x_idx = x_options.index(st.session_state.x_label_val)
    except ValueError:
        x_idx = 3
    
    x_sug = st.selectbox("Common X units", x_options, index=x_idx)
    x_label = st.text_input("Or type custom", value=st.session_state.x_label_val, key="x_input")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", "Runs Scored", "Speed (km/h)"]
    try:
        y_idx = y_options.index(st.session_state.y_label_val)
    except ValueError:
        y_idx = 0
        
    y_sug = st.selectbox("Common Y units", y_options, index=y_idx)
    y_label = st.text_input("Or type custom", value=st.session_state.y_label_val, key="y_input")

# Update state based on current input
st.session_state.x_label_val = x_label
st.session_state.y_label_val = y_label

# ====================== 2. Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio("Select style", 
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True)

# ====================== 3. Data Input ======================
st.subheader("3. Add / Edit Your Data")

# Sample Data
st.markdown("**Sample Data**")
scols = st.columns(4)
with scols[0]:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.x_label_val = "Subjects"
        st.session_state.y_label_val = "Marks"
        st.session_state.data = pd.DataFrame({"Subjects": ["Math","Science","English","History","Geo","Hindi"], "Marks": [85,92,78,65,88,82]})
        st.rerun()
with scols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.x_label_val = "Match No."
        st.session_state.y_label_val = "Runs Scored"
        st.session_state.data = pd.DataFrame({"Match No.": ["M1","M2","M3","M4","M5"], "Runs Scored": [45,78,102,33,67]})
        st.rerun()
with scols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.x_label_val = "Months"
        st.session_state.y_label_val = "Sales (₹)"
        st.session_state.data = pd.DataFrame({"Months": ["Jan","Feb","Mar","Apr","May","Jun"], "Sales (₹)": [45000,52000,48000,61000,55000,68000]})
        st.rerun()
with scols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.x_label_val = "Days"
        st.session_state.y_label_val = "Temperature (°C)"
        st.session_state.data = pd.DataFrame({"Days": [1,2,3,4,5,6], "Temperature (°C)": [28,32,35,31,29,33]})
        st.rerun()

# Edit Data logic
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({x_label: ["Math", "Science", "English"], y_label: [85, 92, 78]})

# KEY ADDITION: Always sync columns with sidebar labels before editing
if list(st.session_state.data.columns) != [x_label, y_label]:
    st.session_state.data.columns = [x_label, y_label]

st.subheader("Edit Your Data")
edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.data = edited_df

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if st.session_state.data.empty:
        st.warning("Please add some data first.")
    else:
        df = st.session_state.data.copy()
        
        # This part is now much safer
        is_num_y = pd.api.types.is_numeric_dtype(df[y_label])

        try:
            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}", markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Box" in graph_choice:
                if not is_num_y: st.error("Box Plot needs numbers in Y"); st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_num_y: st.error("Histogram needs numbers in Y"); st.stop()
                fig = px.histogram(df, x=y_label, nbins=25, title=f"Distribution of {y_label}", opacity=0.9)
                fig.update_traces(marker_color="#1f77b4", marker_line_color="black", marker_line_width=1)

            fig.update_layout(height=700, title_font_size=26, title_x=0.5,
                              xaxis_title=x_label, yaxis_title=y_label,
                              template="plotly_white")

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode()
            st.download_button("💾 Download Data as CSV", csv, "graph_data.csv", "text/csv", use_container_width=True)

        except Exception as e:
            st.error(f"Graph error: {e}")
