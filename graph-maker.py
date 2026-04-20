import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Make your own graph OR upload Excel/CSV**")

# ====================== Labels ======================
st.subheader("1. Set Graph Labels")
col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis Label", value="Time (hours)")
with col2:
    y_label = st.text_input("Y-Axis Label", value="Temperature (°C)")

# ====================== Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_type = st.radio("Select type", 
    ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart", "Box Plot", "Histogram"], 
    horizontal=True)

# ====================== Data Input ======================
st.subheader("3. Enter or Upload Data")

tab1, tab2 = st.tabs(["✏️ Manual Entry (Make Your Own)", "📁 Upload File"])

with tab1:
    st.info("Create your own graph here")
    if 'manual_df' not in st.session_state:
        st.session_state.manual_df = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [10, 25, 35, 48, 62, 75]
        })
    
    manual_edited = st.data_editor(
        st.session_state.manual_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="manual_editor"
    )
    st.session_state.manual_df = manual_edited

with tab2:
    st.info("Upload your CSV or Excel file")
    uploaded = st.file_uploader("Choose file", type=["csv", "xlsx", "xls"])
    
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.success(f"✅ Loaded: {uploaded.name}")
            st.write("**Detected columns:**", list(df.columns))
            
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            
            st.session_state.uploaded_df = df
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Use uploaded data if available, else manual
if 'uploaded_df' in st.session_state and st.session_state.uploaded_df is not None:
    current_df = st.session_state.uploaded_df
    st.info("Using uploaded file data")
else:
    current_df = st.session_state.manual_df

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    df = current_df.copy()
    
    # Clean data (remove empty rows)
    df = df.dropna()
    
    if len(df) == 0:
        st.error("No valid data found.")
        st.stop()
    
    is_y_numeric = pd.api.types.is_numeric_dtype(df.iloc[:, 1])
    
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
            if not is_y_numeric:
                st.error("Box Plot needs numbers in Y column.")
                st.stop()
            fig = px.box(df, y=df.columns[1], title=f"Box Plot of {y_label}")
        elif graph_type == "Histogram":
            if not is_y_numeric:
                st.error("Histogram needs numbers in Y column.")
                st.stop()
            fig = px.histogram(df, x=df.columns[1], nbins=20, title=f"Distribution of {y_label}")

        fig.update_layout(height=650, title_font_size=24)
        st.plotly_chart(fig, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data", csv, "my_graph_data.csv", "text/csv", use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

st.caption("**How to use:** Manual tab = make your own | Upload tab = use your files | Then click Generate Graph")
