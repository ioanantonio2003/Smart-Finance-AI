import sqlite3

# Numele fișierului bazei de date
DB_NAME = "finance_tracker.db"

def init_db():
    """Creează tabelul dacă nu există deja."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Creăm tabelul 'expenses' cu coloanele necesare
    # id: identificator unic
    # date: data bonului
    # category: tipul cheltuielii (Mâncare, Transport, etc.)
    # amount: suma totală
    # description: numele magazinului sau detalii
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Baza de date '{DB_NAME}' a fost inițializată cu succes!")

def add_expense(date, category, amount, description):
    """Adaugă o cheltuială nouă în baza de date."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    
    conn.commit()
    conn.close()
    print(f"✅ Cheltuială adăugată: {description} - {amount} RON")

if __name__ == "__main__":
    # Asta se execută doar când rulăm acest fișier direct
    init_db()