import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")
st.title("📊 Smart Graph Maker")
st.markdown("**Just tell me the units of X and Y axis** — I'll make different types of graphs for you!")

# Sidebar for graph settings
st.sidebar.header("Graph Settings")

# X and Y axis labels (units)
x_label = st.sidebar.text_input("X-Axis Label (Unit)", "Time (seconds)")
y_label = st.sidebar.text_input("Y-Axis Label (Unit)", "Temperature (°C)")

# Graph type selection
graph_type = st.sidebar.selectbox(
    "Choose Graph Type",
    ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart", 
     "Histogram", "Pie Chart", "Box Plot"]
)

# Data input method
data_input = st.radio("How do you want to enter data?", 
                      ["Manual Entry", "Paste from Excel/CSV"])

if data_input == "Manual Entry":
    st.subheader("Enter Your Data")
    
    col1, col2 = st.columns(2)
    with col1:
        x_data = st.text_area(f"Enter {x_label} values (one per line)", 
                             "1\n2\n3\n4\n5\n6")
    with col2:
        y_data = st.text_area(f"Enter {y_label} values (one per line)", 
                             "10\n25\n35\n50\n65\n80")

    try:
        x_values = [float(x.strip()) for x in x_data.strip().split("\n") if x.strip()]
        y_values = [float(y.strip()) for y in y_data.strip().split("\n") if y.strip()]
        
        if len(x_values) != len(y_values):
            st.error("Number of X and Y values must be the same!")
        else:
            df = pd.DataFrame({x_label: x_values, y_label: y_values})
            
    except:
        st.error("Please enter valid numbers only.")

else:
    st.subheader("Paste your data (CSV format)")
    pasted_data = st.text_area("Paste CSV data here (first row = headers)", 
                               "Time,Temperature\n1,10\n2,25\n3,35\n4,50\n5,65")
    try:
        df = pd.read_csv(pd.compat.StringIO(pasted_data))
        x_label = df.columns[0]
        y_label = df.columns[1] if len(df.columns) > 1 else "Value"
    except:
        st.error("Invalid CSV format. First line should be headers.")

# Generate Graph
if 'df' in locals() and not df.empty:
    st.subheader(f"{graph_type} - {y_label} vs {x_label}")
    
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
    elif graph_type == "Pie Chart":
        # For pie, we need categories - using first column as labels if possible
        if len(df.columns) >= 2:
            fig = px.pie(df, names=x_label, values=y_label, title=f"Distribution")
        else:
            st.warning("Pie chart needs categorical data.")
            fig = px.bar(df, x=x_label, y=y_label)
    elif graph_type == "Box Plot":
        fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    st.subheader("Your Data")
    st.dataframe(df, use_container_width=True)
    
    # Download options
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="graph_data.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Enter your data on the left to generate graphs!")

st.caption("Made with ❤️ using Streamlit + Plotly | Just tell the X and Y units and start plotting!")
