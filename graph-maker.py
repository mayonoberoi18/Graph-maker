import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Easy Graph Maker")
st.markdown("**Simple for students** — Upload Excel or type data")

# Step 1: Axis Labels
st.subheader("Step 1: Name your axes")
col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis Label (Bottom line)", value="Days")
with col2:
    y_label = st.text_input("Y-Axis Label (Side line)", value="Marks")

# Step 2: Choose Graph Type (Clear & Simple)
st.subheader("Step 2: Choose Graph Type")
graph_choice = st.radio(
    "Pick one graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# Step 3: Add Data
st.subheader("Step 3: Add your data")

tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Edit in Table"])

with tab1:
    uploaded = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            st.success("✅ File loaded! Using first two columns.")
            # Use first two columns automatically
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()   # take only first 2 columns
                df.columns = [x_label, y_label]   # rename them
            st.session_state.data = df
        except Exception as e:
            st.error(f"Could not read file: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [45, 67, 82, 55, 93, 78]
        })
    
    st.write("Edit or add rows:")
    edited_df = st.data_editor(
        st.session_state.data, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Show data preview
if 'data' in st.session_state:
    st.subheader("Your Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# Step 4: Generate Graph
if st.button("🚀 Generate Graph Now", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please add some data first!")
    else:
        df = st.session_state.data.copy()
        
        # Safety check
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Column names don't match. Please check your data or upload again.")
            st.stop()
        
        # Check if Y is numeric (needed for Histogram & Box Plot)
        try:
            is_y_numeric = pd.api.types.is_numeric_dtype(df[y_label])
        except:
            is_y_numeric = False

        try:
            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Box" in graph_choice:
                if not is_y_numeric:
                    st.error("❌ **Box Plot** needs numbers only in Y-axis. Please choose another graph or change Y data to numbers.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_y_numeric:
                    st.error("❌ **Histogram** needs numbers only in Y-axis. Please choose another graph or use numbers only.")
                    st.stop()
                fig = px.histogram(df, x=y_label, title=f"Histogram of {y_label}")
            
            fig.update_layout(height=650, title_font_size=24)
            st.plotly_chart(fig, use_container_width=True)
            
            # Download option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "my_data.csv", "text/csv")
            
        except Exception as e:
            st.error(f"Error creating graph: {str(e)}")
            st.info("Tip: Make sure X and Y columns contain proper values.")

st.caption("✅ Fixed: Now safe with uploaded Excel files | Choose graph → Click big button")
