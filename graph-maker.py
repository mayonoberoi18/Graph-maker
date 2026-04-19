import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Now intelligently handles your Excel/CSV files**")

# ====================== Units ======================
st.subheader("1. Set Labels for Graph (Optional)")

col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis Label", value="Time (hours)", key="x")
with col2:
    y_label = st.text_input("Y-Axis Label", value="Temperature (°C)", key="y")

if st.button("🔄 Refresh with New Labels", use_container_width=True):
    st.success("Labels updated!")

# ====================== Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio("Select style", 
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"], 
    horizontal=True)

# ====================== Data Input ======================
st.subheader("3. Upload or Edit Data")

uploaded = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded:
    try:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded, engine='openpyxl')
        
        st.success(f"✅ File loaded: **{uploaded.name}**")
        st.write("**Detected Columns:**", list(df.columns))
        
        # Auto use first two columns
        if len(df.columns) >= 2:
            df = df.iloc[:, :2].copy()
            df.columns = ['x_col', 'y_col']   # Internal names
            st.info("Using first two columns from your file.")
        
        st.session_state.data = df
        st.rerun()
        
    except Exception as e:
        st.error(f"Could not read file: {e}")

# Sample Data (for testing)
if st.button("Load Sample Time vs Temperature"):
    st.session_state.data = pd.DataFrame({
        'x_col': [1,2,3,4,5,6,7,8],
        'y_col': [10,25,35,48,62,75,80,95]
    })
    st.rerun()

# Edit Data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({'x_col': [1,2,3,4], 'y_col': [10,25,35,48]})

st.subheader("Edit Data")
edited = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.data = edited

st.subheader("Data Preview")
st.dataframe(st.session_state.data, use_container_width=True)

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("No data available. Upload a file or use sample.")
    else:
        df = st.session_state.data.copy()
        
        # Rename for plotting using user labels
        plot_df = df.rename(columns={'x_col': x_label, 'y_col': y_label})
        
        is_numeric = pd.api.types.is_numeric_dtype(df['y_col'])

        try:
            if "Line" in graph_choice:
                fig = px.line(plot_df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}", markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(plot_df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Scatter" in graph_choice:
                fig = px.scatter(plot_df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Area" in graph_choice:
                fig = px.area(plot_df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Box" in graph_choice:
                if not is_numeric:
                    st.error("Box Plot needs numbers in Y column.")
                    st.stop()
                fig = px.box(plot_df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric:
                    st.error("Histogram needs numbers in Y column.")
                    st.stop()
                fig = px.histogram(plot_df, x=y_label, nbins=20, title=f"Distribution of {y_label}", opacity=0.85)
                fig.update_traces(marker_color="#1f77b4", marker_line_width=1.5)

            fig.update_layout(
                height=700,
                title_font_size=26,
                title_x=0.5,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

            csv = plot_df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "my_graph_data.csv", "text/csv", use_container_width=True)

            st.success("Graph generated successfully!")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: Make sure your Y column contains only numbers (no empty rows).")

st.caption("Upload your file → Edit if needed → Choose graph type → Click Generate Graph")
