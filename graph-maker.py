import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="My Fun Graph Maker", page_icon="🎨", layout="wide")

st.title("🎨 My Fun Graph Maker")
st.markdown("### For Kids! Make colorful pictures with numbers")

# Step 1 & 2 - Very big and simple
st.subheader("1. What is on the bottom line?")
x_name = st.text_input("", value="Days", label_visibility="collapsed")

st.subheader("2. What is on the tall line?")
y_name = st.text_input("", value="Candies", label_visibility="collapsed")

# Step 3 - Fun graph choices
st.subheader("3. What kind of picture do you want?")
graph_type = st.selectbox(
    "",
    ["📈 Line (Connecting dots)", 
     "📊 Bar (Tall boxes)", 
     "🌟 Scatter (Dots everywhere)", 
     "🏠 Area (Filled color)"],
    label_visibility="collapsed"
)

# Step 4 - Upload Excel or type numbers
st.subheader("4. Add your numbers")

col1, col2 = st.columns(2)

with col1:
    if st.button("📁 Upload Excel or CSV File", use_container_width=True):
        uploaded_file = st.file_uploader("Choose your Excel (.xlsx) or CSV file", 
                                       type=["xlsx", "xls", "csv"], 
                                       label_visibility="collapsed")
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Use first two columns automatically
                if len(df.columns) >= 2:
                    df.columns = [x_name, y_name]   # rename to match user labels
                st.session_state.my_data = df
                st.success("✅ File loaded! Now click 'Make My Graph'")
            except:
                st.error("Sorry, I couldn't read this file. Try a simple Excel with two columns.")

with col2:
    if st.button("✏️ Type Numbers Myself", use_container_width=True):
        if 'my_data' not in st.session_state:
            st.session_state.my_data = pd.DataFrame({
                x_name: [1, 2, 3, 4, 5],
                y_name: [5, 10, 15, 25, 40]
            })

# Show and edit the table
if 'my_data' in st.session_state:
    st.write("Edit the numbers if you want:")
    edited_data = st.data_editor(
        st.session_state.my_data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.my_data = edited_data
else:
    st.info("Click 'Upload Excel' or 'Type Numbers Myself' to start 😊")

# Big Magic Button
if st.button("✨ Make My Graph Now!", type="primary", use_container_width=True):
    if 'my_data' in st.session_state and not st.session_state.my_data.empty:
        df = st.session_state.my_data
        
        # Choose graph type
        if "Line" in graph_type:
            fig = px.line(df, x=x_name, y=y_name, title=f"My {y_name} over {x_name}")
        elif "Bar" in graph_type:
            fig = px.bar(df, x=x_name, y=y_name, title=f"My {y_name} over {x_name}")
        elif "Scatter" in graph_type:
            fig = px.scatter(df, x=x_name, y=y_name, title=f"My {y_name} over {x_name}")
        else:
            fig = px.area(df, x=x_name, y=y_name, title=f"My {y_name} over {x_name}")
        
        fig.update_layout(height=550, title_font_size=26, font=dict(size=18))
        
        st.plotly_chart(fig, use_container_width=True)
        st.balloons()
        
        # Download buttons
        csv = df.to_csv(index=False).encode()
        st.download_button("💾 Download My Numbers (CSV)", csv, "my_fun_data.csv", "text/csv")
        
    else:
        st.warning("Please add some numbers first!")

st.caption("Easy for kids: Upload Excel → Edit numbers → Click big button → See magic graph! 🎈")
