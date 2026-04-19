import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("### Make beautiful graphs instantly — Upload Excel • Change units • Edit easily")

# ====================== 1. AXIS UNITS ======================
st.subheader("1. Choose Your Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis (Bottom)**")
    x_common = ["Days", "Months", "Time (hours)", "Time (seconds)", "Subjects", 
                "Match No.", "Age (years)", "Distance (km)"]
    x_sug = st.selectbox("Common X units", x_common, index=4)
    x_label = st.text_input("Custom X unit", value=x_sug, key="x_input")

with col2:
    st.markdown("**Y-Axis (Side)**")
    y_common = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                "Speed (km/h)", "Weight (kg)", "Runs Scored", "Price (₹)"]
    y_sug = st.selectbox("Common Y units", y_common, index=0)
    y_label = st.text_input("Custom Y unit", value=y_sug, key="y_input")

if st.button("🔄 Refresh Data with New Units", type="secondary", use_container_width=True):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("✅ Data updated with new units!")

# ====================== 2. GRAPH TYPE ======================
st.subheader("2. Select Graph Type")
graph_choice = st.radio(
    "Choose graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True,
    label_visibility="collapsed"
)

# ====================== 3. DATA SECTION ======================
st.subheader("3. Your Data")

# Sample Data
st.markdown("**Quick Samples**")
cols = st.columns(4)
with cols[0]:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Math", "Science", "English", "History", "Geography", "Hindi"],
            y_label: [85, 92, 78, 65, 88, 82]
        })
        st.rerun()
with cols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["M1", "M2", "M3", "M4", "M5"],
            y_label: [45, 78, 102, 33, 67]
        })
        st.rerun()
with cols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y_label: [45000, 52000, 48000, 61000, 55000, 68000]
        })
        st.rerun()
with cols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [28, 32, 35, 31, 29, 33]
        })
        st.rerun()

# File Upload
st.subheader("Upload Your Excel or CSV File")
uploaded_file = st.file_uploader("Select file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.success(f"✅ File loaded: **{uploaded_file.name}**")
        st.write("**Original Columns:**", list(df.columns))
        
        if len(df.columns) >= 2:
            df = df.iloc[:, :2].copy()
            df.columns = [x_label, y_label]
            st.info("✅ Using first two columns from your file.")
        
        st.session_state.data = df
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Could not read file: {str(e)}")
        st.info("Tip: Make sure the file is not empty and saved as .xlsx format.")

# Edit Data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        x_label: ["Math", "Science", "English"],
        y_label: [85, 92, 78]
    })

st.subheader("Edit Your Data")
st.info("You can change names in X column and numbers in Y column.")

edited_data = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.data = edited_data

# Preview
st.subheader("Data Preview")
st.dataframe(st.session_state.data, use_container_width=True)

# ====================== GENERATE GRAPH ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please upload a file or load sample data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Please click 'Refresh Data with New Units' after changing units.")
            st.stop()

        is_numeric_y = pd.api.types.is_numeric_dtype(df[y_label])

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
                if not is_numeric_y:
                    st.error("Box Plot requires numeric Y values.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot — {y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric_y:
                    st.error("Histogram requires numeric Y values.")
                    st.stop()
                fig = px.histogram(
                    df, x=y_label, nbins=25, 
                    title=f"Distribution of {y_label}",
                    opacity=0.85
                )
                fig.update_traces(marker_color="#3498db", marker_line_color="#2c3e50", marker_line_width=1.5)

            # Final Professional Touch
            fig.update_layout(
                height=720,
                title_font_size=28,
                title_x=0.5,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                font=dict(size=14),
                margin=dict(l=80, r=40, t=100, b=80)
            )

            fig.update_xaxes(title_font=dict(size=18), tickfont=dict(size=13))
            fig.update_yaxes(title_font=dict(size=18), tickfont=dict(size=13))

            st.plotly_chart(fig, use_container_width=True)

            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Download Data as CSV",
                data=csv,
                file_name="my_graph_data.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.success("✅ Professional graph generated successfully!")

        except Exception as e:
            st.error(f"Error creating graph: {e}")

st.caption("Best Version • Easy Excel Support • Professional Graphs • Made with ❤️")
