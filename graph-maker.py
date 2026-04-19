import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graph Maker", page_icon="📊", layout="wide")

st.title("📊 Graph Maker (Stable Version)")

# ================= FILE UPLOAD =================
uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded is not None:
    try:
        # Read file
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded, engine="openpyxl")

        # Clean
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        st.success("File loaded successfully!")

        # ================= PREVIEW =================
        st.subheader("Data Preview")
        st.dataframe(df)

        # ================= COLUMN SELECTION =================
        columns = df.columns.tolist()

        x_col = st.selectbox("Select X-axis", columns)
        y_col = st.selectbox("Select Y-axis", columns)

        graph_type = st.selectbox(
            "Graph Type",
            ["Line", "Bar", "Scatter", "Area", "Box", "Histogram"]
        )

        # ================= GRAPH =================
        if st.button("Generate Graph"):

            plot_df = df[[x_col, y_col]].copy()

            # Convert Y to numeric safely
            plot_df[y_col] = pd.to_numeric(plot_df[y_col], errors="coerce")
            plot_df = plot_df.dropna()

            if len(plot_df) == 0:
                st.error("No valid numeric data found")
                st.stop()

            # Create graph
            if graph_type == "Line":
                fig = px.line(plot_df, x=x_col, y=y_col, markers=True)

            elif graph_type == "Bar":
                fig = px.bar(plot_df, x=x_col, y=y_col)

            elif graph_type == "Scatter":
                fig = px.scatter(plot_df, x=x_col, y=y_col)

            elif graph_type == "Area":
                fig = px.area(plot_df, x=x_col, y=y_col)

            elif graph_type == "Box":
                fig = px.box(plot_df, y=y_col)

            elif graph_type == "Histogram":
                fig = px.histogram(plot_df, x=y_col, nbins=20)

            fig.update_layout(title=f"{y_col} vs {x_col}", title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            # Download CSV
            csv = plot_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "data.csv")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Upload a file to start")
