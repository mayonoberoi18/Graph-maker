import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Simple Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Simple & Reliable Graph Maker")
st.markdown("Upload your CSV/Excel → Choose graph type → Generate")

# File Upload
st.subheader("Upload Your File")
uploaded = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded:
    try:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.success(f"✅ File loaded: **{uploaded.name}**")
        st.write("**Columns detected:**", list(df.columns))

        # Use first two columns
        if len(df.columns) < 2:
            st.error("File must have at least 2 columns.")
            st.stop()

        df = df.iloc[:, :2].copy()
        actual_x_col = df.columns[0]
        actual_y_col = df.columns[1]

        st.session_state.raw_data = df
        st.session_state.actual_x = actual_x_col
        st.session_state.actual_y = actual_y_col

    except Exception as e:
        st.error(f"Failed to read file: {e}")

# Display and Edit Data
if 'raw_data' in st.session_state:
    st.subheader("Your Data (First 2 columns)")
    edited_df = st.data_editor(
        st.session_state.raw_data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.raw_data = edited_df

    # Labels for graph display
    st.subheader("Graph Labels (You can change these)")
    col1, col2 = st.columns(2)
    with col1:
        display_x = st.text_input("X-Axis Label", value=st.session_state.actual_x)
    with col2:
        display_y = st.text_input("Y-Axis Label", value=st.session_state.actual_y)

    # Graph Type
    st.subheader("Choose Graph Type")
    graph_type = st.radio("Select type:", 
        ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart", "Box Plot", "Histogram"],
        horizontal=True)

    if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
        df = st.session_state.raw_data.copy()
        
        # Rename for nice display
        plot_df = df.rename(columns={df.columns[0]: display_x, df.columns[1]: display_y})
        
        y_is_number = pd.api.types.is_numeric_dtype(df.iloc[:, 1])

        try:
            if graph_type == "Line Chart":
                fig = px.line(plot_df, x=display_x, y=display_y, title=f"{display_y} vs {display_x}", markers=True)
            elif graph_type == "Bar Chart":
                fig = px.bar(plot_df, x=display_x, y=display_y, title=f"{display_y} vs {display_x}")
            elif graph_type == "Scatter Plot":
                fig = px.scatter(plot_df, x=display_x, y=display_y, title=f"{display_y} vs {display_x}")
            elif graph_type == "Area Chart":
                fig = px.area(plot_df, x=display_x, y=display_y, title=f"{display_y} vs {display_x}")
            elif graph_type == "Box Plot":
                if not y_is_number:
                    st.error("Box Plot needs numbers in the second column.")
                    st.stop()
                fig = px.box(plot_df, y=display_y, title=f"Box Plot of {display_y}")
            elif graph_type == "Histogram":
                if not y_is_number:
                    st.error("Histogram needs numbers in the second column.")
                    st.stop()
                fig = px.histogram(plot_df, x=display_y, nbins=20, title=f"Distribution of {display_y}")

            fig.update_layout(height=650, title_font_size=24)
            st.plotly_chart(fig, use_container_width=True)

            # Download
            csv_download = plot_df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Edited Data", csv_download, "graph_data.csv", "text/csv")

        except Exception as e:
            st.error(f"Could not create graph: {e}")
else:
    st.info("👆 Please upload your CSV or Excel file to begin.")

st.caption("Tip: Your first file has 'Time (hours)' and 'Temperature (°C)'. Second file has 'time' and 'temperature'.")
