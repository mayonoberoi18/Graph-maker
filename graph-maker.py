import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Easy Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Professional Graph Maker")
st.markdown("**Clean • Professional • Easy to use** — Change units anytime")

# Step 1: Units
st.subheader("Step 1: Set X and Y Axis Units")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Students", 
                 "Games Played", "Distance (km)", "Temperature (°C)"]
    x_suggestion = st.selectbox("Common X units", x_options, index=0)
    x_label = st.text_input("Custom X unit", value=x_suggestion, key="x_input")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", 
                 "Speed (km/h)", "Weight (kg)", "Runs", "Candies", "Price (₹)"]
    y_suggestion = st.selectbox("Common Y units", y_options, index=0)
    y_label = st.text_input("Custom Y unit", value=y_suggestion, key="y_input")

# Step 2: Graph Type
st.subheader("Step 2: Choose Graph Type")
graph_choice = st.radio(
    "Select graph style:",
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", 
     "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True
)

# Step 3: Your Data Section
st.subheader("Step 3: Your Data")

# Sample Data Buttons
st.markdown("**Quick Load Samples**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Math", "Science", "English", "History", "Geo", "Hindi"],
            y_label: [85, 92, 78, 65, 88, 82]
        })
        st.success("Loaded!")
with c2:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["M1", "M2", "M3", "M4", "M5"],
            y_label: [45, 78, 102, 33, 67]
        })
        st.success("Loaded!")
with c3:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y_label: [45000, 52000, 48000, 61000, 55000, 68000]
        })
        st.success("Loaded!")
with c4:
    if st.button("📏 Height Growth", use_container_width=True):
        st.session_state.data = pd.DataFrame({
            x_label: [10, 11, 12, 13, 14, 15],
            y_label: [135, 142, 148, 155, 162, 168]
        })
        st.success("Loaded!")

# Data Input
tab1, tab2 = st.tabs(["📁 Upload Excel/CSV", "✏️ Edit Data"])

with tab1:
    uploaded = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = [x_label, y_label]
            st.success("✅ File loaded!")
            st.session_state.data = df
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            x_label: [1, 2, 3, 4, 5, 6],
            y_label: [45, 67, 82, 55, 93, 78]
        })
    
    st.write("**Edit your data below:**")
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.data = edited_df

# Data Preview
if 'data' in st.session_state:
    st.subheader("Your Current Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# Generate Professional Graph
if st.button("🚀 Generate Professional Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please add data first!")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Column mismatch. Please check data.")
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
                    st.error("Box Plot needs numbers in Y-axis.")
                    st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot — {y_label}")
            elif "Histogram" in graph_choice:
                if not is_y_numeric:
                    st.error("Histogram needs numbers in Y-axis.")
                    st.stop()
                # Professional Histogram
                fig = px.histogram(df, x=y_label, title=f"Distribution of {y_label}",
                                 nbins=15, opacity=0.85)

            # Professional Styling for All Graphs
            fig.update_layout(
                height=700,
                title_font_size=28,
                title_x=0.5,
                font_family="Arial",
                font_size=14,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template="plotly_white",
                plot_bgcolor="rgba(255,255,255,1)",
                paper_bgcolor="rgba(255,255,255,1)",
                margin=dict(l=80, r=40, t=80, b=80)
            )

            # Enhanced Axis Styling (clear units)
            fig.update_xaxes(
                title_font=dict(size=18, color="black"),
                tickfont=dict(size=14),
                showgrid=True,
                gridcolor="rgba(200,200,200,0.5)",
                linecolor="black",
                linewidth=1
            )
            fig.update_yaxes(
                title_font=dict(size=18, color="black"),
                tickfont=dict(size=14),
                showgrid=True,
                gridcolor="rgba(200,200,200,0.5)",
                linecolor="black",
                linewidth=1
            )

            # Special improvements for Histogram
            if "Histogram" in graph_choice:
                fig.update_traces(
                    marker_color="#636EFA",
                    marker_line_color="black",
                    marker_line_width=1.5
                )

            st.plotly_chart(fig, use_container_width=True, theme=None)

            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Data as CSV", csv, "professional_graph_data.csv", "text/csv", use_container_width=True)

            st.success("✅ Professional graph generated!")

        except Exception as e:
            st.error(f"Error: {e}")

st.caption("💡 Change X or Y units anytime and regenerate the graph. Units now appear clearly on axes.")
