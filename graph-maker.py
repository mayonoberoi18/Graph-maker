import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Upload Excel • Change Units • Edit Data • Professional Graphs**")

# ====================== SESSION STATE INITIALIZATION ======================
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'x': ["Math", "Science", "English", "History"],
        'y': [85, 92, 78, 65]
    })
if 'x_label' not in st.session_state:
    st.session_state.x_label = "Subjects"
if 'y_label' not in st.session_state:
    st.session_state.y_label = "Marks"

# ====================== 1. AXIS UNITS ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Time (seconds)", "Subjects", 
                 "Match No.", "Age (years)", "Distance (km)"]
    x_sug = st.selectbox("Common X units", x_options, index=4, key="x_sug")
    x_label = st.text_input("Or type your own X unit", value=x_sug, key="x_input")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Speed (km/h)", "Weight (kg)", "Runs Scored", "Price (₹)"]
    y_sug = st.selectbox("Common Y units", y_options, index=0, key="y_sug")
    y_label = st.text_input("Or type your own Y unit", value=y_sug, key="y_input")

# Update labels when changed
st.session_state.x_label = x_label
st.session_state.y_label = y_label

if st.button("🔄 Refresh Data with New Units", type="secondary", use_container_width=True):
    st.success("✅ Units updated! You can now generate the graph.")

# ====================== 2. GRAPH TYPE ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio(
    "Select style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== 3. DATA INPUT ======================
st.subheader("3. Your Data")

# Sample Data
st.markdown("**Quick Sample Data**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({'x': ["Math","Science","English","History","Geo","Hindi"], 'y': [85,92,78,65,88,82]})
        st.rerun()
with c2:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({'x': ["M1","M2","M3","M4","M5"], 'y': [45,78,102,33,67]})
        st.rerun()
with c3:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({'x': ["Jan","Feb","Mar","Apr","May","Jun"], 'y': [45000,52000,48000,61000,55000,68000]})
        st.rerun()
with c4:
    if st.button("🌡️ Temperature Over Time", use_container_width=True):
        st.session_state.data = pd.DataFrame({'x': [1,2,3,4,5,6], 'y': [28,32,35,31,29,33]})
        st.rerun()

# Upload File
st.subheader("Upload Your Excel or CSV File")
uploaded = st.file_uploader("Choose your file", type=["xlsx", "xls", "csv"])

if uploaded:
    try:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded, engine='openpyxl')
        
        st.success(f"✅ File **{uploaded.name}** loaded successfully!")
        
        if len(df.columns) >= 2:
            df = df.iloc[:, :2].copy()
            df.columns = ['x', 'y']
            st.info("Using first two columns from your file.")
        else:
            st.warning("File has less than 2 columns. Using as is.")
        
        st.session_state.data = df
        st.rerun()
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")
        st.info("Tip: Save your file as .xlsx and make sure it has data.")

# Edit Data
st.subheader("Edit Your Data")
st.info("✅ Change subject names in left column and numbers in right column.")

edited = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.data = edited

st.subheader("Data Preview")
st.dataframe(st.session_state.data, use_container_width=True)

# ====================== GENERATE GRAPH ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    if st.session_state.data.empty:
        st.warning("Please add data first!")
    else:
        df = st.session_state.data.copy()
        
        # Rename internal columns to user labels for plotting
        plot_df = df.rename(columns={'x': st.session_state.x_label, 'y': st.session_state.y_label})
        
        is_numeric_y = pd.api.types.is_numeric_dtype(df['y'])

        try:
            title = f"{st.session_state.y_label} vs {st.session_state.x_label}"

            if "Line" in graph_choice:
                fig = px.line(plot_df, x=st.session_state.x_label, y=st.session_state.y_label, title=title, markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(plot_df, x=st.session_state.x_label, y=st.session_state.y_label, title=title)
            elif "Scatter" in graph_choice:
                fig = px.scatter(plot_df, x=st.session_state.x_label, y=st.session_state.y_label, title=title)
            elif "Area" in graph_choice:
                fig = px.area(plot_df, x=st.session_state.x_label, y=st.session_state.y_label, title=title)
            elif "Box" in graph_choice:
                if not is_numeric_y:
                    st.error("Box Plot needs numbers in Y-axis.")
                    st.stop()
                fig = px.box(plot_df, y=st.session_state.y_label, title=f"Box Plot of {st.session_state.y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric_y:
                    st.error("Histogram needs numbers in Y-axis.")
                    st.stop()
                fig = px.histogram(plot_df, x=st.session_state.y_label, nbins=25, 
                                 title=f"Distribution of {st.session_state.y_label}", opacity=0.85)
                fig.update_traces(marker_color="#3498db", marker_line_color="#2c3e50", marker_line_width=1.5)

            # Professional styling
            fig.update_layout(
                height=720,
                title_font_size=28,
                title_x=0.5,
                xaxis_title=st.session_state.x_label,
                yaxis_title=st.session_state.y_label,
                template="plotly_white",
                margin=dict(l=80, r=50, t=100, b=80)
            )
            fig.update_xaxes(title_font=dict(size=18), tickfont=dict(size=14))
            fig.update_yaxes(title_font=dict(size=18), tickfont=dict(size=14))

            st.plotly_chart(fig, use_container_width=True)

            # Download CSV
            csv = plot_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Download Data as CSV",
                data=csv,
                file_name="my_graph_data.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.success("✅ Professional graph created successfully!")

        except Exception as e:
            st.error(f"Error generating graph: {e}")

st.caption("This is the complete best version. All features work reliably. Upload your Excel file and enjoy!")
