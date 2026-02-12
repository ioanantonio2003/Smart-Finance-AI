import streamlit as st
from PIL import Image
from ai_logic import analyze_receipt
from database import add_expense, get_all_expenses # <--- Am importat si functia noua
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configurare Pagină
st.set_page_config(page_title="Smart Finance AI", page_icon="💰", layout="wide")

st.title("💰 Smart Finance Assistant")

# 2. Inițializare Session State
if 'ai_data' not in st.session_state:
    st.session_state.ai_data = None

# --- PARTEA 1: UPLOAD & AI ---
with st.sidebar:
    st.header("Upload Receipt")
    uploaded_file = st.file_uploader("Choose a receipt image...", type=["jpg", "jpeg", "png"])
    st.info("Supported formats: JPG, PNG")

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Your Receipt")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("⚡ Analyze Receipt with AI", type="primary"):
            with st.spinner("🤖 AI is reading the receipt... please wait..."):
                try:
                    extracted_data = analyze_receipt(image)
                    if extracted_data:
                        st.session_state.ai_data = extracted_data
                        st.toast("Analysis Complete!", icon="✅")
                    else:
                        st.error("AI could not extract data.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        st.subheader("📝 Extracted Details")
        if st.session_state.ai_data:
            with st.form("expense_form"):
                data_init = st.session_state.ai_data.get('date') or ""
                merchant_init = st.session_state.ai_data.get('merchant') or ""
                amount_raw = st.session_state.ai_data.get('amount')
                try:
                    amount_float = float(amount_raw) if amount_raw else 0.0
                except:
                    amount_float = 0.0
                cat_init = st.session_state.ai_data.get('category') or "Other"
                
                date_val = st.text_input("Date (YYYY-MM-DD)", value=data_init)
                merchant_val = st.text_input("Merchant/Store", value=merchant_init)
                amount_val = st.number_input("Total Amount (RON)", value=amount_float, step=0.01)
                
                lista_categorii = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Other"]
                idx = 5
                if cat_init in lista_categorii:
                    idx = lista_categorii.index(cat_init)
                
                category_val = st.selectbox("Category", lista_categorii, index=idx)

                if st.form_submit_button("💾 Save to Database"):
                    add_expense(date_val, category_val, amount_val, merchant_val)
                    st.success("✅ Expense saved successfully!")
                    st.session_state.ai_data = None
                    st.rerun()
        else:
            st.info("Upload an image and click 'Analyze' to see the magic happen here.")

# --- PARTEA 2: ANALYTICS & HISTORY ---
st.markdown("---")
st.header("📊 Spending Overview")

# Încărcăm datele din baza de date
data = get_all_expenses()

if data:
    # Creăm un DataFrame Pandas (tabel inteligent)
    df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Amount", "Description"])
    
    # Facem două coloane: Grafic stânga, Tabel dreapta
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("Expenses by Category")
        # Grupăm sumele pe categorii
        category_totals = df.groupby("Category")["Amount"].sum()
        
        # Facem un Pie Chart cu Matplotlib
        fig, ax = plt.subplots()
        ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') # Asigură că e cerc perfect
        st.pyplot(fig)
        
        st.metric("Total Spent", f"{df['Amount'].sum():.2f} RON")

    with col_right:
        st.subheader("Recent Transactions")
        # Afișăm tabelul frumos, fără coloana ID
        st.dataframe(df[["Date", "Category", "Description", "Amount"]], use_container_width=True)
else:
    st.info("No expenses saved yet. Upload a receipt to start tracking!")