import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker Pro", page_icon="📊", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Graph Maker")
st.markdown("**Change Units • Edit Data • Make Graphs • By Mayon Oberoi**")

# ====================== 1. Initialization ======================
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({"Subjects": ["Math", "Science", "English"], "Marks": [85, 92, 78]})
    st.session_state.old_x = "Subjects"
    st.session_state.old_y = "Marks"

# ====================== 2. Axis Configuration ======================
with st.sidebar:
    st.header("⚙️ Settings")
    
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", "Age (years)", "Distance (km)"]
    x_label = st.selectbox("X-Axis Label", x_options, index=3)
    custom_x = st.text_input("Or type custom X", value="")
    final_x = custom_x if custom_x else x_label

    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", "Runs Scored", "Speed (km/h)"]
    y_label = st.selectbox("Y-Axis Label", y_options, index=0)
    custom_y = st.text_input("Or type custom Y", value="")
    final_y = custom_y if custom_y else y_label

    # Sync dataframe columns with labels automatically
    if final_x != st.session_state.data.columns[0] or final_y != st.session_state.data.columns[1]:
        st.session_state.data.columns = [final_x, final_y]

# ====================== 3. Graph Type ======================
st.subheader("1. Choose Graph Type")
graph_choice = st.radio("Select style", 
    ["📈 Line", "📊 Bar", "🌟 Scatter", "🏠 Area", "📦 Box", "📊 Histogram"],
    horizontal=True)

# ====================== 4. Data Input ======================
st.subheader("2. Add / Edit Your Data")

scols = st.columns(4)
samples = {
    "🏫 School Marks": {"x": ["Math","Science","English","History"], "y": [85,92,78,65]},
    "🏏 Cricket Runs": {"x": ["M1","M2","M3","M4"], "y": [45,78,102,33]},
    "💰 Monthly Sales": {"x": ["Jan","Feb","Mar","Apr"], "y": [45000,52000,48000,61000]},
    "🌡️ Temperature": {"x": [1,2,3,4], "y": [28,32,35,31]}
}

for i, (name, content) in enumerate(samples.items()):
    with scols[i]:
        if st.button(name):
            st.session_state.data = pd.DataFrame({final_x: content["x"], final_y: content["y"]})
            st.rerun()

edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="editor"
)
st.session_state.data = edited_df

# ====================== 5. Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary"):
    df = st.session_state.data
    
    try:
        if "Line" in graph_choice:
            fig = px.line(df, x=final_x, y=final_y, markers=True)
        elif "Bar" in graph_choice:
            fig = px.bar(df, x=final_x, y=final_y, color=final_y, color_continuous_scale="Viridis")
        elif "Scatter" in graph_choice:
            fig = px.scatter(df, x=final_x, y=final_y, size=final_y, color=final_y)
        elif "Area" in graph_choice:
            fig = px.area(df, x=final_x, y=final_y)
        elif "Box" in graph_choice:
            fig = px.box(df, y=final_y)
        elif "Histogram" in graph_choice:
            fig = px.histogram(df, x=final_y, nbins=15)

        fig.update_layout(
            template="plotly_white",
            title=dict(text=f"{final_y} Analysis", font=dict(size=24), x=0.5),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Download section
        csv = df.to_csv(index=False).encode()
        st.download_button("💾 Download CSV", csv, "data.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Please ensure your data matches the selected chart type! Error: {e}")
