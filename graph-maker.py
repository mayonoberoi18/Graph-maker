import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📈", layout="wide")

st.title("📈 Cool Graph Maker")
st.markdown("### Make awesome graphs in seconds — Just add labels and data")

# Sidebar for settings
st.sidebar.header("Graph Settings")

x_label = st.sidebar.text_input("X-Axis Label", value="Days", 
                                help="Example: Time (hours), Subjects, Months, Players")

y_label = st.sidebar.text_input("Y-Axis Label", value="Score", 
                                help="Example: Marks, Speed (km/h), Sales (₹), Height (cm)")

graph_type = st.sidebar.selectbox(
    "Choose Graph Type",
    ["Line Chart", "Bar Chart", "Scatter Plot", 
     "Area Chart", "Histogram", "Box Plot"]
)

# Main Area
st.subheader("Add Your Data")

# Two easy ways: Upload or Manual
tab1, tab2 = st.tabs(["📁 Upload Excel / CSV", "✏️ Type or Edit Data"])

with tab1:
    uploaded_file = st.file_uploader("Upload your Excel (.xlsx) or CSV file", 
                                    type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ File uploaded successfully!")
            st.session_state.data = df
        except:
            st.error("Could not read the file. Make sure it has data in columns.")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6, 7],
            y_label: [45, 62, 78, 55, 89, 95, 82]
        })
    
    st.write("Edit the table below:")
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Show current data
if 'data' in st.session_state:
    st.subheader("Your Data Preview")
    st.dataframe(st.session_state.data, use_container_width=True)

# Big Generate Button
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if 'data' in st.session_state and not st.session_state.data.empty:
        df = st.session_state.data
        
        # Choose graph
        if graph_type == "Line Chart":
            fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif graph_type == "Bar Chart":
            fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif graph_type == "Scatter Plot":
            fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif graph_type == "Area Chart":
            fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
        elif graph_type == "Histogram":
            fig = px.histogram(df, x=y_label, title=f"Distribution of {y_label}")
        elif graph_type == "Box Plot":
            fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
        
        # Make it look cool
        fig.update_layout(
            height=600,
            title_font_size=24,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Download options
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Data as CSV", 
                             csv, "my_graph_data.csv", "text/csv")
        
        st.success("Graph created! You can zoom, hover, and save the image using the camera icon on the graph.")
        
    else:
        st.warning("Please upload a file or add some data first.")

st.caption("Made for students | Easy Excel support | No coding needed")
