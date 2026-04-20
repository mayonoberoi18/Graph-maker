import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Graph Maker")
st.markdown("**Change Units • Edit Data • Make Graphs• By Mayon Oberoi • Illuminati**")

# ====================== 1. Units ======================
st.subheader("1. Set X and Y Axis Units")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**X-Axis Label**")
    x_options = ["Days", "Months", "Time (hours)", "Subjects", "Match No.", "Age (years)", "Distance (km)"]
    x_sug = st.selectbox("Common X units", x_options, index=3)
    x_label = st.text_input("Or type custom", value=x_sug, key="x")

with col2:
    st.markdown("**Y-Axis Label**")
    y_options = ["Marks", "Score", "Temperature (°C)", "Sales (₹)", "Height (cm)", "Runs Scored", "Speed (km/h)"]
    y_sug = st.selectbox("Common Y units", y_options, index=0)
    y_label = st.text_input("Or type custom", value=y_sug, key="y")

if st.button("🔄 Refresh Data with New Units", use_container_width=True):
    if 'data' in st.session_state:
        st.session_state.data.columns = [x_label, y_label]
        st.success("Units updated successfully!")

# ====================== 2. Graph Type ======================
st.subheader("2. Choose Graph Type")
graph_choice = st.radio("Select style", 
    ["📈 Line Chart", "📊 Bar Chart", "🌟 Scatter Plot", "🏠 Area Chart", "📦 Box Plot", "📊 Histogram"],
    horizontal=True)

# ====================== 3. Data Input ======================
st.subheader("3. Add / Edit Your Data")

# Sample Data
st.markdown("**Sample Data**")
scols = st.columns(4)
with scols[0]:
    if st.button("🏫 School Marks", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: ["Math","Science","English","History","Geo","Hindi"], y_label: [85,92,78,65,88,82]})
        st.rerun()
with scols[1]:
    if st.button("🏏 Cricket Runs", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: ["M1","M2","M3","M4","M5"], y_label: [45,78,102,33,67]})
        st.rerun()
with scols[2]:
    if st.button("💰 Monthly Sales", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: ["Jan","Feb","Mar","Apr","May","Jun"], y_label: [45000,52000,48000,61000,55000,68000]})
        st.rerun()
with scols[3]:
    if st.button("🌡️ Temperature", use_container_width=True):
        st.session_state.data = pd.DataFrame({x_label: [1,2,3,4,5,6], y_label: [28,32,35,31,29,33]})
        st.rerun()



# Edit Data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({x_label: ["Math", "Science", "English"], y_label: [85, 92, 78]})

st.subheader("Edit Your Data")
st.info("Change subject names in left column and numbers in right column.")

edited_df = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.data = edited_df

if 'data' in st.session_state:
    st.subheader("Data Preview")
    st.dataframe(st.session_state.data, use_container_width=True)

# ====================== Generate Graph ======================
if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.warning("Please upload file or load sample data")
    else:
        df = st.session_state.data.copy()
        
        if x_label not in df.columns or y_label not in df.columns:
            st.error("Click 'Refresh Data with New Units' after changing units.")
            st.stop()

        is_num_y = pd.api.types.is_numeric_dtype(df[y_label])

        try:
            if "Line" in graph_choice:
                fig = px.line(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}", markers=True)
            elif "Bar" in graph_choice:
                fig = px.bar(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Scatter" in graph_choice:
                fig = px.scatter(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Area" in graph_choice:
                fig = px.area(df, x=x_label, y=y_label, title=f"{y_label} vs {x_label}")
            elif "Box" in graph_choice:
                if not is_num_y: st.error("Box Plot needs numbers in Y"); st.stop()
                fig = px.box(df, y=y_label, title=f"Box Plot of {y_label}")
            elif "Histogram" in graph_choice:
                if not is_num_y: st.error("Histogram needs numbers in Y"); st.stop()
                fig = px.histogram(df, x=y_label, nbins=25, title=f"Distribution of {y_label}", opacity=0.9)
                fig.update_traces(marker_color="#1f77b4", marker_line_color="black", marker_line_width=1)

            fig.update_layout(height=700, title_font_size=26, title_x=0.5,
                              xaxis_title=x_label, yaxis_title=y_label,
                              template="plotly_white")

            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode()
            st.download_button("💾 Download Data as CSV", csv, "graph_data.csv", "text/csv", use_container_width=True)

        except Exception as e:
            st.error(f"Graph error: {e}")

st.caption("You can also download the data.")
