import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Make your own graph • Upload files • Change units easily**")

# ====================== 1. Units with Refresh Button ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    x_label = st.text_input("X-Axis Label", value="Time (hours)", key="x_label")
with col2:
    y_label = st.text_input("Y-Axis Label", value="Temperature (°C)", key="y_label")

# Refresh Button - Very Important
if st.button("🔄 Refresh Data with New Units", type="secondary", use_container_width=True):
    st.success("✅ Units updated! Now generate the graph again.")
    if 'data' in st.session_state:
        # Update column names if data exists
        if len(st.session_state.data.columns) >= 2:
            st.session_state.data.columns = [x_label, y_label]

# ====================== 2. Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_type = st.radio("Select graph style:", 
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"], 
    horizontal=True)

# ====================== 3. Data Input ======================
st.subheader("3. Your Data")

tab1, tab2 = st.tabs(["✏️ Manual Entry (Make Your Own)", "📁 Upload Excel/CSV"])

with tab1:
    st.info("Create your own data here")
    if 'manual_data' not in st.session_state:
        st.session_state.manual_data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6, 7, 8],
            y_label: [10, 25, 35, 48, 62, 75, 80, 95]
        })
    
    edited_manual = st.data_editor(
        st.session_state.manual_data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="manual_key"
    )
    st.session_state.manual_data = edited_manual

with tab2:
    st.info("Upload your file")
    uploaded = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx", "xls"])
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.success(f"✅ File loaded: {uploaded.name}")
            st.write("**Columns in file:**", list(df.columns))
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]   # Apply current labels
            st.session_state.upload_data = df
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

# Decide which data to use
if 'upload_data' in st.session_state and st.session_state.upload_data is not None:
    current_data = st.session_state.upload_data
    st.info("📁 Using uploaded file data")
else:
    current_data = st.session_state.manual_data
    st.info("✏️ Using manual entry data")

# ====================== Generate Graph ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    df = current_data.copy().dropna()   # Remove empty rows
    
    if len(df) == 0:
        st.error("No data to plot. Please add some data.")
        st.stop()

    try:
        if graph_type == "Line Chart":
            fig = px.line(df, x=df.columns[0], y=df.columns[1], title=f"{y_label} vs {x_label}", markers=True)
        elif graph_type == "Bar Chart":
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=f"{y_label} vs {x_label}")
        elif graph_type == "Scatter Plot":
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=f"{y_label} vs {x_label}")
        elif graph_type == "Area Chart":
            fig = px.area(df, x=df.columns[0], y=df.columns[1], title=f"{y_label} vs {x_label}")
        elif graph_type == "Box Plot":
            fig = px.box(df, y=df.columns[1], title=f"Box Plot of {y_label}")
        elif graph_type == "Histogram":
            fig = px.histogram(df, x=df.columns[1], nbins=20, title=f"Distribution of {y_label}", opacity=0.85)

        # Beautiful styling
        fig.update_layout(
            height=680,
            title_font_size=26,
            title_x=0.5,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data as CSV", csv, "my_graph_data.csv", "text/csv", use_container_width=True)

        st.success("✅ Graph created successfully!")

    except Exception as e:
        st.error(f"Could not generate graph: {e}")
        st.info("Tip: Make sure your Y column has numbers only.")

st.caption("How to change units: Change the labels above → Click **'Refresh Data with New Units'** → Generate Graph again")
