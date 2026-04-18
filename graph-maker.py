import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")
st.title("📊 Easy Graph Maker")
st.markdown("### Just tell me the X and Y axis units and add your data — I'll create beautiful graphs for you!")

# Instructions
with st.expander("📋 How to Use This App (Super Simple)", expanded=True):
    st.markdown("""
    1. **Enter X-axis Label** (e.g., Time (seconds), Month, Student Name)
    2. **Enter Y-axis Label** (e.g., Temperature (°C), Sales (₹), Height (cm))
    3. Choose how to add data:
       - Click **"Load Sample Data"** to try immediately
       - Type data manually
       - Or **upload** your CSV/Excel file
    4. Select the Graph Type you like
    5. Watch the graph appear instantly!

    **Tip:** Hover over the graph to see values. You can zoom and download the image too!
    """)

# Sidebar - Axis Labels and Graph Type
st.sidebar.header("🎯 Graph Settings")

x_label = st.sidebar.text_input("X-Axis Label (Unit)", value="Time (hours)", help="Example: Time (seconds), Category, Month")
y_label = st.sidebar.text_input("Y-Axis Label (Unit)", value="Temperature (°C)", help="Example: Sales (₹), Speed (km/h), Score")

graph_type = st.sidebar.selectbox(
    "Choose Graph Type",
    ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart", 
     "Histogram", "Box Plot", "Pie Chart"]
)

# Main area - Data Input
st.subheader("📥 Add Your Data")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📊 Load Sample Data (Try Now)"):
        sample_data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6, 7, 8],
            y_label: [10, 25, 35, 48, 62, 75, 80, 95]
        })
        st.session_state.df = sample_data
        st.success("Sample data loaded! Change labels above if needed.")

with col2:
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx", "xls"])

# Data entry options
data_method = st.radio("How do you want to enter data?", 
                       ["Use Sample / Uploaded Data", "Manual Entry (Table)"], horizontal=True)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.success(f"File uploaded successfully! Columns: {list(df.columns)}")
    except Exception as e:
        st.error(f"Error reading file: {e}")

if data_method == "Manual Entry (Table)":
    st.info("Edit the table below directly")
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5],
            y_label: [10, 20, 30, 40, 50]
        })
    edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
    st.session_state.df = edited_df
else:
    if 'df' in st.session_state:
        st.dataframe(st.session_state.df, use_container_width=True)
    else:
        st.info("Click 'Load Sample Data' or upload a file to begin.")

# Generate Graph
if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df
    
    # Auto-detect columns if labels don't match
    x_col = df.columns[0] if x_label not in df.columns else x_label
    y_col = df.columns[1] if len(df.columns) > 1 and y_label not in df.columns else y_label
    
    st.subheader(f"📈 Your {graph_type}")
    
    try:
        if graph_type == "Line Chart":
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_label} vs {x_label}")
        elif graph_type == "Bar Chart":
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_label} vs {x_label}")
        elif graph_type == "Scatter Plot":
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_label} vs {x_label}")
        elif graph_type == "Area Chart":
            fig = px.area(df, x=x_col, y=y_col, title=f"{y_label} vs {x_label}")
        elif graph_type == "Histogram":
            fig = px.histogram(df, x=y_col, title=f"Distribution of {y_label}")
        elif graph_type == "Box Plot":
            fig = px.box(df, y=y_col, title=f"Box Plot of {y_label}")
        elif graph_type == "Pie Chart":
            if len(df.columns) >= 2:
                fig = px.pie(df, names=x_col, values=y_col, title="Pie Chart")
            else:
                fig = px.bar(df, x=x_col, y=y_col)
        
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=600,
            title_font_size=20
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Download buttons
        col_a, col_b = st.columns(2)
        with col_a:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Data as CSV", csv, "my_graph_data.csv", "text/csv")
        with col_b:
            st.caption("💡 Tip: Hover on graph → Click camera icon to download image")
            
    except Exception as e:
        st.error(f"Could not create graph. Error: {e}")
        st.info("Tip: Make sure your data has numbers in the Y column.")

else:
    st.info("👆 Please load sample data, upload a file, or enter data manually to see the graph.")

st.caption("Made easy for everyone | No coding needed | Just labels + data = Graph!")
