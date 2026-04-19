import streamlit as st
import pandas as pd
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(page_title="Graph Maker Pro", page_icon="📊", layout="wide")

st.title("📊 Graph Maker Pro (Stable Version)")
st.write("Create graphs easily — upload, edit, and download")

# ================= SESSION STATE =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "X": [1, 2, 3, 4, 5],
        "Y": [10, 20, 30, 40, 50]
    })

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")

x_label = st.sidebar.text_input("X Axis Label", value="X")
y_label = st.sidebar.text_input("Y Axis Label", value="Y")

graph_type = st.sidebar.selectbox("Graph Type", [
    "Line", "Bar", "Scatter", "Area", "Box", "Histogram"
])

theme = st.sidebar.selectbox("Theme", [
    "plotly", "plotly_white", "plotly_dark"
])

# ================= DATA INPUT =================
st.subheader("📥 Data Input")

tab1, tab2 = st.tabs(["Manual Entry", "Upload File"])

with tab1:
    edited = st.data_editor(
        st.session_state.data,
        num_rows="dynamic",
        use_container_width=True
    )
    st.session_state.data = edited

with tab2:
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

            if df.shape[1] < 2:
                st.error("File must have at least 2 columns")
            else:
                df = df.iloc[:, :2]
                df.columns = [x_label, y_label]
                st.session_state.data = df
                st.success("File loaded successfully!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

# ================= DATA PREVIEW =================
df = st.session_state.data.copy()

if df.shape[1] >= 2:
    df.columns = [x_label, y_label]

st.subheader("📋 Data Preview")
st.dataframe(df, use_container_width=True)

# ================= GRAPH =================
st.subheader("📈 Graph")

if st.button("Generate Graph 🚀"):

    df = df.dropna()

    if len(df) == 0:
        st.error("No valid data")
        st.stop()

    try:
        title = f"{y_label} vs {x_label}"

        # ---------- GRAPH LOGIC ----------
        if graph_type == "Line":
            fig = px.line(df, x=x_label, y=y_label, markers=True)

        elif graph_type == "Bar":
            fig = px.bar(df, x=x_label, y=y_label)

        elif graph_type == "Scatter":
            fig = px.scatter(df, x=x_label, y=y_label)

        elif graph_type == "Area":
            fig = px.area(df, x=x_label, y=y_label)

        elif graph_type == "Box":
            if not pd.api.types.is_numeric_dtype(df[y_label]):
                st.error("Y must be numeric for Box Plot")
                st.stop()
            fig = px.box(df, y=y_label)

        elif graph_type == "Histogram":
            if not pd.api.types.is_numeric_dtype(df[y_label]):
                st.error("Y must be numeric for Histogram")
                st.stop()
            fig = px.histogram(df, x=y_label, nbins=20)

        # ---------- STYLING ----------
        fig.update_layout(
            template=theme,
            title=title,
            title_x=0.5,
            height=600,
            xaxis_title=x_label,
            yaxis_title=y_label
        )

        st.plotly_chart(fig, use_container_width=True)

        # ================= DOWNLOAD =================
        st.subheader("⬇ Download")

        col1, col2 = st.columns(2)

        with col1:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "data.csv")

        with col2:
            try:
                img = fig.to_image(format="png")
                st.download_button("Download PNG", img, "graph.png")
            except:
                st.warning("PNG download needs kaleido installed")

        st.success("Graph created successfully!")

    except Exception as e:
        st.error(f"Error generating graph: {e}")
