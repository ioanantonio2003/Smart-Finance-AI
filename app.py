import streamlit as st

# Configurare pagină (Titlu tab, iconiță, layout)
st.set_page_config(page_title="Smart Finance AI", page_icon="💰")

# Titlul principal din pagină
st.title("💰 Smart Finance Assistant")
st.subheader("Upload a receipt to track your expenses automatically")

# Sidebar (Meniul din stânga)
st.sidebar.header("Options")
uploaded_file = st.sidebar.file_uploader("Choose a receipt image...", type=["jpg", "jpeg", "png"])

# Zona principală
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Receipt", use_column_width=True)
    st.success("File uploaded successfully! AI processing pending...")
else:
    st.info("Please upload a receipt image to get started.")