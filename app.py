import streamlit as st
from PIL import Image
from ai_logic import analyze_receipt  # Importăm logica AI reparată
from database import add_expense      # Importăm logica bazei de date

# 1. Configurare Pagină
st.set_page_config(page_title="Smart Finance AI", page_icon="💰", layout="wide")

st.title("💰 Smart Finance Assistant")
st.markdown("---")

# 2. Inițializare Session State
if 'ai_data' not in st.session_state:
    st.session_state.ai_data = None

# 3. Sidebar pentru Upload
with st.sidebar:
    st.header("Upload Receipt")
    uploaded_file = st.file_uploader("Choose a receipt image...", type=["jpg", "jpeg", "png"])
    st.info("Supported formats: JPG, PNG")

# 4. Logica Principală
if uploaded_file is not None:
    col1, col2 = st.columns(2)

    # Coloana 1: Imaginea
    with col1:
        st.subheader("📸 Your Receipt")
        # Deschidem imaginea
        image = Image.open(uploaded_file)
        
        # Afișăm imaginea corect (fără warning)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Butonul de Analiză
        if st.button("⚡ Analyze Receipt with AI", type="primary"):
            with st.spinner("🤖 AI is reading the receipt... please wait..."):
                try:
                    # Trimitem imaginea la funcția din ai_logic.py
                    extracted_data = analyze_receipt(image)
                    
                    if extracted_data:
                        st.session_state.ai_data = extracted_data
                        st.toast("Analysis Complete!", icon="✅")
                    else:
                        st.error("AI could not extract data. Check terminal for details.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Coloana 2: Formularul
    with col2:
        st.subheader("📝 Extracted Details")
        
        if st.session_state.ai_data:
            with st.form("expense_form"):
                # Extragem valorile cu protecție (dacă lipsesc)
                data_initiala = st.session_state.ai_data.get('date') or ""
                merchant_initial = st.session_state.ai_data.get('merchant') or ""
                
                # Gestionăm suma
                amount_raw = st.session_state.ai_data.get('amount')
                try:
                    amount_float = float(amount_raw) if amount_raw else 0.0
                except:
                    amount_float = 0.0

                # Gestionăm categoria
                cat_initiala = st.session_state.ai_data.get('category') or "Other"
                
                # Input-uri
                date_val = st.text_input("Date (YYYY-MM-DD)", value=data_initiala)
                merchant_val = st.text_input("Merchant/Store", value=merchant_initial)
                amount_val = st.number_input("Total Amount (RON)", value=amount_float, step=0.01)
                
                # Dropdown Categorie
                lista_categorii = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Other"]
                idx = 5 # Default Other
                if cat_initiala in lista_categorii:
                    idx = lista_categorii.index(cat_initiala)
                
                category_val = st.selectbox("Category", lista_categorii, index=idx)

                # Buton Salvare
                submitted = st.form_submit_button("💾 Save to Database")

                if submitted:
                    add_expense(date_val, category_val, amount_val, merchant_val)
                    st.success("✅ Expense saved successfully!")
                    st.session_state.ai_data = None
                    st.rerun()
        else:
            st.info("Upload an image and click 'Analyze' to see the magic happen here.")

else:
    st.markdown("### 👋 Welcome! Upload a receipt to start.")