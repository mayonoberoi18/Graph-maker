import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Easy & Beautiful Graph Maker")
st.markdown("**Professional graphs in seconds • Change units easily**")

# ====================== Step 1: Units ======================
st.subheader("Step 1: Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis (Bottom)**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Students", 
                 "Games Played", "Distance (km)", "Temperature (°C)"]
    x_suggestion = st.selectbox("Common X units", x_options, index=0)
    x_label = st.text_input("Or type custom X unit", value=x_suggestion, key="x_input")

with col2:
    st.markdown("**Y-Axis (Side)**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Speed (km/h)", "Weight (kg)", "Runs", "Candies"]
    y_suggestion = st.selectbox("Common Y units", y_options, index=0)
    y_label = st.text_input("Or type custom Y unit", value=y_suggestion, key="y_input")

# ====================== Step 2: Graph Type ======================
st.subheader("Step 2: Choose Graph Type")
graph_choice = st.radio(
    "Select graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== Step 3: Your Data Section ======================
st.subheader("Step 3: Your Data")

# Sample Data Buttons
st.markdown("**Quick Start: Load Sample Data**")
sample_col1, sample_col2, sample_col3, sample_col4 = st.columns(4)

with sample_col1:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Math", "Science", "English", "History", "Geography", "Hindi"],
            y_label: [85, 92, 78, 65, 88, 82]
        })
        st.success("School Marks loaded!")

with sample_col2:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Match 1", "Match 2", "Match 3", "Match 4", "Match 5"],
            y_label: [45, 78, 102, 33, 67]
        })
        st.success("Cricket Runs loaded!")

with sample_col3:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y_label: [45000, 52000, 48000, 61000, 55000, 68000]
        })
        st.success("Monthly Sales loaded!")

with sample_col4:
    if st.button("📏 Height Growth", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: [10, 11, 12, 13, 14, 15],
            y_label: [135, 142, 148, 155, 162, 168]
        })
        st.success("Height Growth loaded!")

# Data Input Tabs
tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Edit Data"])

with tab1:
    uploaded = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            st.success("✅ File uploaded successfully!")
            st.session_state.data = df
        except Exception as e:
            st.error(f"Could not read file: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [45, 67, 82, 55, 93, 78]
        })
    
    st.write("**Edit your data here** (add/delete rows as needed):")
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Data Preview
if 'data' in st.session_state:
    st.subheader("Your Current Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# ====================== Generate Graph ======================
if st.button("🚀 Generate Beautiful Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please load sample data, upload a file, or enter data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Column names don't match. Please check your data.")
            st.stop()

        is_y_numeric = pd.api.types.is_numeric_dtype(df[y_label])

        try:
            title = f"{y_label} vs {x_label}"

            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=title, markers=True, line_shape="linear")
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=title, color_discrete_sequence=["#636EFA"])
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=title, color_discrete_sequence=["#EF553B"])
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=title)
            elif "Box" in graph_choice:
                if not is_y_numeric:
                    st.error("❌ Box Plot needs numbers in the Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_y_numeric:
                    st.error("❌ Histogram needs numbers in the Y-axis.")
                    st.stop()
                fig = px.histogram(df, x=y_label, title=f"Histogram of {y_label}", nbins=10)

            # Beautiful Graph Improvements
            fig.update_layout(
                height=680,
                title_font_size=28,
                title_x=0.5,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                font=dict(size=14),
                showlegend=True,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            # Add gridlines and better styling
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

            st.plotly_chart(fig, use_container_width=True)

            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Your Data as CSV", 
                             csv, "my_graph_data.csv", "text/csv", use_container_width=True)

            st.success("✅ Graph generated successfully!")

        except Exception as e:
            st.error(f"Error generating graph: {e}")
            st.info("Tip: Make sure your data has valid numbers where needed.")

st.caption("💡 Tip: You can change X and Y units anytime and click 'Generate Beautiful Graph' again.")
