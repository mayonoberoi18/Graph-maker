import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Easy & Beautiful Graph Maker")
st.markdown("**Change units easily • Upload Excel • Make pro-looking graphs**")

# ================== Step 1: Units / Labels ==================
st.subheader("Step 1: Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Unit (Bottom)**")
    common_x = ["Days", "Months", "Time (hours)", "Time (seconds)", "Subjects", 
                "Students", "Games", "Distance (km)", "Temperature (°C)", "Price (₹)"]
    x_suggestion = st.selectbox("Common X units", common_x, index=0)
    x_label = st.text_input("Or type your own X unit", value=x_suggestion)

with col2:
    st.markdown("**Y-Axis Unit (Side)**")
    common_y = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                "Speed (km/h)", "Weight (kg)", "Candies", "Runs", "Students", "Price (₹)"]
    y_suggestion = st.selectbox("Common Y units", common_y, index=0)
    y_label = st.text_input("Or type your own Y unit", value=y_suggestion)

# ================== Step 2: Graph Type ==================
st.subheader("Step 2: Choose Graph Style")
graph_choice = st.radio(
    "Select graph type:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True,
    label_visibility="visible"
)

# ================== Step 3: Data Input ==================
st.subheader("Step 3: Add Your Data")

tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Edit Data in Table"])

with tab1:
    uploaded = st.file_uploader("Upload your file here", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            # Take only first two columns and rename
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            st.success("✅ File uploaded and columns updated!")
            st.session_state.data = df
        except Exception as e:
            st.error(f"Error reading file: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6, 7],
            y_label: [45, 67, 82, 55, 93, 78, 88]
        })
    
    st.write("Add or change numbers here:")
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Data Preview
if 'data' in st.session_state:
    st.subheader("Your Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# ================== Generate Graph ==================
if st.button("🚀 Generate Beautiful Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please add some data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Column mismatch. Please upload file again or edit table.")
            st.stop()

        is_y_numeric = pd.api.types.is_numeric_dtype(df[y_label])

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
                if not is_y_numeric:
                    st.error("Box Plot and Histogram require numbers in Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot - {y_label}")
            elif "Histogram" in graph_choice:
                if not is_y_numeric:
                    st.error("Box Plot and Histogram require numbers in Y-axis.")
                    st.stop()
                fig = px.histogram(df, x=y_label, title=f"Histogram of {y_label}")

            # Improve graph appearance
            fig.update_layout(
                height=650,
                title_font_size=26,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                hoverlabel=dict(font_size=14)
            )
            
            # Nice colors
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

            st.plotly_chart(fig, use_container_width=True)

            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "my_graph_data.csv", "text/csv")

        except Exception as e:
            st.error(f"Could not create graph: {e}")

st.caption("✅ You can change units anytime • Works great with Excel files • Beautiful graphs")
