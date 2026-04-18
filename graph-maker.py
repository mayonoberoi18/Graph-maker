import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Easy Graph Maker")
st.markdown("**Super simple for students** — Upload Excel or type data")

# Step 1: Axis Labels
st.subheader("Step 1: Name your axes")
col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis Label (Bottom)", value="Days", help="Example: Days, Month, Subject")
with col2:
    y_label = st.text_input("Y-Axis Label (Side)", value="Marks", help="Example: Score, Height (cm), Sales (₹)")

# Step 2: Choose Graph Type (Big & Clear)
st.subheader("Step 2: Choose Graph Type")
graph_choice = st.radio(
    "Pick the style you want:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# Step 3: Add Data
st.subheader("Step 3: Add your data")

tab1, tab2 = st.tabs(["📁 Upload Excel or CSV", "✏️ Edit Table"])

with tab1:
    uploaded = st.file_uploader("Choose file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.success("✅ File loaded successfully!")
            st.session_state.data = df
        except:
            st.error("Could not read file. Please use a simple Excel/CSV with data.")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [45, 67, 82, 55, 93, 78]
        })
    
    st.write("Edit or add rows here:")
    edited_df = st.data_editor(
        st.session_state.data, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Show data
if 'data' in st.session_state:
    st.subheader("Your Current Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# Step 4: Generate Button
if st.button("🚀 Generate Graph Now", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please add some data first!")
    else:
        df = st.session_state.data.copy()
        
        # Check if Y column is numeric (important for Histogram & Box Plot)
        is_y_numeric = pd.api.types.is_numeric_dtype(df[y_label])
        
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
                    st.error("❌ Box Plot needs numbers in Y-axis. Please choose another graph or change Y data to numbers.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_y_numeric:
                    st.error("❌ Histogram needs numbers in Y-axis. Please choose another graph or use numbers only.")
                    st.stop()
                fig = px.histogram(df, x=y_label, title=f"Histogram of {y_label}")
            
            fig.update_layout(height=650, title_font_size=24)
            st.plotly_chart(fig, use_container_width=True)
            
            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "my_data.csv", "text/csv")
            
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.info("Tip: Make sure your X and Y columns have proper data.")

st.caption("Tip: For Histogram & Box Plot, Y-axis must have only numbers.")
