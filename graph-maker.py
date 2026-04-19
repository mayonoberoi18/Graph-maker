import streamlit as st
import pandas as pd
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(page_title="Ultimate Graph Maker Pro", page_icon="📊", layout="wide")

st.title("📊 Ultimate Graph Maker Pro Max")
st.markdown("Upload • Analyze • Visualize • Compare")

# ================= SESSION =================
if "df" not in st.session_state:
    st.session_state.df = None

# ================= SIDEBAR =================
st.sidebar.header("📁 Upload Data")

file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

# ================= LOAD DATA =================
if file:
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")

        # Clean data
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        st.session_state.df = df
        st.success("File loaded successfully!")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# ================= MAIN =================
if st.session_state.df is not None:

    df = st.session_state.df.copy()

    st.subheader("📋 Data Preview")
    st.dataframe(df, use_container_width=True)

    # ================= SETTINGS =================
    st.sidebar.header("⚙️ Graph Settings")

    columns = df.columns.tolist()

    x_col = st.sidebar.selectbox("X-axis", columns)

    y_cols = st.sidebar.multiselect("Y-axis (Select multiple)", columns, default=[columns[1]] if len(columns)>1 else columns)

    graph_type = st.sidebar.selectbox(
        "Graph Type",
        ["Line", "Bar", "Scatter", "Area", "Box", "Histogram"]
    )

    theme = st.sidebar.selectbox(
        "Theme",
        ["plotly", "plotly_white", "plotly_dark", "ggplot2"]
    )

    color = st.sidebar.color_picker("Pick Graph Color", "#1f77b4")

    add_trendline = st.sidebar.checkbox("Add Trendline (Line/Scatter only)")

    # ================= FILTER =================
    st.sidebar.header("🔍 Filter Data")

    if st.sidebar.checkbox("Enable Filtering"):
        unique_vals = df[x_col].unique()
        selected_vals = st.sidebar.multiselect("Filter X values", unique_vals, default=unique_vals)
        df = df[df[x_col].isin(selected_vals)]

    # ================= GRAPH =================
    st.subheader("📈 Graph")

    if st.button("Generate Graph 🚀"):

        try:
            if len(df) == 0:
                st.error("No data after filtering")
                st.stop()

            plot_df = df[[x_col] + y_cols].copy()

            # Convert numeric safely
            for col in y_cols:
                plot_df[col] = pd.to_numeric(plot_df[col], errors="coerce")

            plot_df = plot_df.dropna()

            if len(plot_df) == 0:
                st.error("No valid numeric data")
                st.stop()

            # Melt for multi-column plotting
            plot_df = plot_df.melt(id_vars=x_col, var_name="Variable", value_name="Value")

            title = "Graph"

            # ---------- GRAPH TYPES ----------
            if graph_type == "Line":
                fig = px.line(plot_df, x=x_col, y="Value", color="Variable",
                              markers=True,
                              trendline="ols" if add_trendline else None)

            elif graph_type == "Bar":
                fig = px.bar(plot_df, x=x_col, y="Value", color="Variable")

            elif graph_type == "Scatter":
                fig = px.scatter(plot_df, x=x_col, y="Value", color="Variable",
                                 trendline="ols" if add_trendline else None)

            elif graph_type == "Area":
                fig = px.area(plot_df, x=x_col, y="Value", color="Variable")

            elif graph_type == "Box":
                fig = px.box(plot_df, y="Value", color="Variable")

            elif graph_type == "Histogram":
                fig = px.histogram(plot_df, x="Value", color="Variable", nbins=20)

            # ---------- STYLE ----------
            fig.update_layout(
                template=theme,
                height=700,
                title=title,
                title_x=0.5
            )

            # Apply color (only for single variable)
            if len(y_cols) == 1:
                fig.update_traces(marker_color=color)

            st.plotly_chart(fig, use_container_width=True)

            # ================= DOWNLOAD =================
            st.subheader("⬇ Download")

            col1, col2 = st.columns(2)

            with col1:
                csv = plot_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "data.csv")

            with col2:
                try:
                    img = fig.to_image(format="png")
                    st.download_button("Download PNG", img, "graph.png")
                except:
                    st.warning("Install kaleido for PNG export")

            st.success("Graph generated successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("👆 Upload a file to begin")
