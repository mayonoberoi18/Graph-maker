import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pro Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Pro Graph Maker")
st.markdown("**Upload your Excel file easily • Professional graphs**")

# ====================== 1. Axis Units ======================
st.subheader("1. Set Your Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_label = st.text_input("X-Axis Label", value="Subjects", key="x_key")

with col2:
    st.markdown("**Y-Axis Label**")
    y_label = st.text_input("Y-Axis Label", value="Marks", key="y_key")

if st.button("🔄 Refresh Data with New Units", type="secondary"):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("✅ Units updated!")

# ====================== 2. Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio(
    "Select graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# ====================== 3. Your Data ======================
st.subheader("3. Your Data")

# Sample buttons (optional)
st.markdown("**Or load sample data**")
if st.button("🏫 School Marks Example"):
    st.session_state.data = pd.DataFrame({
        x_label: ["Math", "Science", "English", "History"],
        y_label: [85, 92, 78, 65]
    })
    st.rerun()

# Upload Section - Improved for Excel
st.subheader("Upload Your Excel / CSV File")
uploaded = st.file_uploader("Choose your Excel (.xlsx) or CSV file", 
                           type=["xlsx", "xls", "csv"])

if uploaded:
    try:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded, engine='openpyxl')
        
        st.success(f"✅ File '{uploaded.name}' loaded successfully!")
        
        # Show original columns
        st.write("**Columns in your file:**", list(df.columns))
        
        # Take first two columns and rename to user's labels
        if len(df.columns) >= 2:
            df = df.iloc[:, :2].copy()          # Keep only first 2 columns
            df.columns = [x_label, y_label]     # Rename to user's choice
            st.success("Using first two columns from your file.")
        else:
            st.warning("File has less than 2 columns. Using as is.")
        
        st.session_state.data = df
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Could not read your file. Error: {str(e)}")
        st.info("Tips: Make sure your Excel file has data in the first two columns. Try saving as .xlsx (not .xls).")

# Manual Edit Tab
tab1, tab2 = st.tabs(["📁 Uploaded / Sample Data", "✏️ Edit Data"])

with tab1:
    if 'data' in st.session_state:
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("Upload your Excel file or load sample above.")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: ["Item 1", "Item 2", "Item 3"],
            y_label: [45, 67, 82]
        })
    
    st.write("**Edit your data here:**")
    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited

# ====================== Generate Graph ======================
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please upload your Excel file or enter some data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Please click 'Refresh Data with New Units' after changing labels.")
            st.stop()

        is_numeric_y = pd.api.types.is_numeric_dtype(df[y_label])

        try:
            title = f"{y_label} vs {x_label}"

            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=title, markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=title)
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=title)
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=title)
            elif "Box" in graph_choice:
                if not is_numeric_y:
                    st.error("Box Plot needs numbers in Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_numeric_y:
                    st.error("Histogram needs numbers in Y-axis.")
                    st.stop()
                fig = px.histogram(df, x=y_label, nbins=20, title=f"Distribution of {y_label}", opacity=0.85)
                fig.update_traces(marker_color="#3498db", marker_line_color="#2c3e50", marker_line_width=1.5)

            # Professional styling
            fig.update_layout(
                height=720,
                title_font_size=28,
                title_x=0.5,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "my_graph_data.csv", "text/csv", use_container_width=True)

        except Exception as e:
            st.error(f"Error generating graph: {e}")
            st.info("Tip: Make sure your Y column contains only numbers.")

st.caption("Upload your Excel file → It will use the first two columns → Edit if needed → Generate Graph")
