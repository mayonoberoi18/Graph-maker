import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Easy Graph Maker")
st.markdown("**For students** — Make any graph in 4 simple steps")

# Step 1: Labels
st.subheader("Step 1: Name your axes")
col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("X-Axis (Bottom line)", value="Days")
with col2:
    y_label = st.text_input("Y-Axis (Side line)", value="Marks")

# Step 2: Choose Graph Type with big buttons
st.subheader("Step 2: Choose Graph Type")
graph_choice = st.radio(
    "Pick one:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True,
    label_visibility="collapsed"
)

# Clean name for code
graph_type = graph_choice.split(" ", 1)[1]   # removes emoji

# Step 3: Add Data
st.subheader("Step 3: Add your data")

tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Edit in Table"])

with tab1:
    uploaded = st.file_uploader("Upload your file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.success("File loaded!")
            st.session_state.data = df
        except:
            st.error("Sorry, couldn't read the file. Try a simple Excel with 2 columns.")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [50, 65, 78, 55, 92, 85]
        })
    
    st.write("You can add or change numbers here:")
    edited = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)
    st.session_state.data = edited

# Show data preview
if 'data' in st.session_state:
    st.subheader("Your Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# Step 4: Big Generate Button
if st.button("🚀 Create My Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please add some data first!")
    else:
        df = st.session_state.data
        
        # Create the graph based on choice
        if "Line" in graph_choice:
            fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif "Bar" in graph_choice:
            fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif "Scatter" in graph_choice:
            fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif "Area" in graph_choice:
            fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif "Box" in graph_choice:
            fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
        elif "Histogram" in graph_choice:
            fig = px.histogram(df, x=y_label, title=f"Histogram of {y_label}")
        
        fig.update_layout(height=650, title_font_size=22)
        
        st.plotly_chart(fig, use_container_width=True)
        st.balloons()

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Data as CSV", csv, "my_data.csv", "text/csv")

st.caption("Tip: Upload Excel → Choose graph type → Click big button. Very easy!")
