import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Fixed version** - Change units • Edit data • Generate graph")

# ====================== 1. Units ======================
st.subheader("1. X and Y Axis Labels")

col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis Label", value="Time (hours)", key="x_label_key")
with col2:
    y_label = st.text_input("Y-Axis Label", value="Temperature (°C)", key="y_label_key")

# ✅ FIX: actually update dataframe column names
if st.button("🔄 Refresh with New Units", type="secondary", use_container_width=True):
    if 'current_data' in st.session_state:
        df = st.session_state.current_data.copy()
        if df.shape[1] >= 2:
            df.columns = [x_label, y_label]
            st.session_state.current_data = df
    st.success("Labels updated successfully!")

# ====================== 2. Graph Type ======================
st.subheader("2. Graph Type")
graph_type = st.radio("Choose graph:", 
    ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart", "Box Plot", "Histogram"], 
    horizontal=True)

# ====================== 3. Data ======================
st.subheader("3. Your Data")

# Initialize data if not exists
if 'current_data' not in st.session_state:
    st.session_state.current_data = pd.DataFrame({
        x_label: [1, 2, 3, 4, 5, 6],
        y_label: [10, 25, 35, 48, 62, 75]
    })

# Manual + Upload in one place for simplicity
tab1, tab2 = st.tabs(["Manual Entry", "Upload File"])

with tab1:
    st.info("Edit here - You can change numbers and text")
    edited_data = st.data_editor(
        st.session_state.current_data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.current_data = edited_data

with tab2:
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.success("File loaded!")
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            st.session_state.current_data = df
            st.dataframe(df)
        except Exception as e:
            st.error(f"Could not read file: {e}")

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    df = st.session_state.current_data.copy()
    
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    if len(df) < 1:
        st.error("Please add some data.")
        st.stop()

    # Ensure column names match labels
    df.columns = [x_label, y_label]

    # ✅ NEW: Safe numeric check before plotting
    y_numeric = pd.api.types.is_numeric_dtype(df[y_label])

    try:
        if graph_type == "Line Chart":
            fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}", markers=True)

        elif graph_type == "Bar Chart":
            fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")

        elif graph_type == "Scatter Plot":
            fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")

        elif graph_type == "Area Chart":
            fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")

        elif graph_type == "Box Plot":
            if not y_numeric:
                st.error("Box Plot needs numeric Y values.")
                st.stop()
            fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")

        elif graph_type == "Histogram":
            if not y_numeric:
                st.error("Histogram needs numeric Y values.")
                st.stop()
            fig = px.histogram(df, x=y_label, nbins=20, title=f"Distribution of {y_label}", opacity=0.85)

        # Professional look
        fig.update_layout(
            height=680,
            title_font_size=26,
            title_x=0.5,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data as CSV", csv, "graph_data.csv", "text/csv", use_container_width=True)

        # ✅ NEW: PNG Download (safe)
        try:
            img = fig.to_image(format="png")
            st.download_button("🖼 Download Graph as PNG", img, "graph.png", use_container_width=True)
        except:
            st.info("Install 'kaleido' to enable PNG download")

        st.success("Graph generated successfully!")

    except Exception as e:
        st.error(f"Could not generate graph: {e}")

st.caption("Change X/Y labels → Click Refresh → Edit data → Generate Graph")
