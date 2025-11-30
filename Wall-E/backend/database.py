import os
import sqlite3

# 📌 Ma'lumotlar bazasi joylashuvi
DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "containers.db")

# 📌 Agar "data" papkasi mavjud bo‘lmasa, yaratamiz
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

def get_db_connection():
    """SQLITE bazasiga ulanish"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Natijani lug‘at sifatida qaytarish uchun
    return conn

def init_db():
    """Bazani yaratish va dastlabki konteynerlarni qo'shish"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 📌 **Konteynerlar jadvalini yaratamiz**
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS containers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            max_weight REAL NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    """)

    # 📌 Jadval bo‘shligini tekshiramiz
    cursor.execute("SELECT COUNT(*) FROM containers")
    count = cursor.fetchone()[0]

    # 📌 Faqat ma'lumotlar bazasi bo‘sh bo‘lsa, test ma’lumotlarini qo‘shamiz
    if count == 0:
        containers_data = [
            ("Toshkent ", 50, 100, 41.2995, 69.2401),
            ("Samarqand ", 75, 150, 39.6543, 66.9759),
            ("Buxoro ", 90, 150, 39.7686, 64.4559),  
            ("Xiva ", 30, 100, 41.3785, 60.3630),
            ("Nukus ", 80, 80, 42.4600, 59.6000),  # To‘lgan
            ("Andijon ", 60, 250, 40.7833, 72.3500),
            ("Namangan ", 45, 100, 40.9983, 71.6726),
            ("Farg'ona ", 100, 100, 40.3864, 71.7843),  # To‘lgan
        ]

        cursor.executemany("""
            INSERT INTO containers (name, weight, max_weight, lat, lon) VALUES (?, ?, ?, ?, ?)
        """, containers_data)
        print("✅Containers have been added!")

    conn.commit()
    conn.close()
    print("✅ The database is ready!")

# 📌 Skript mustaqil ishga tushganda bazani yaratamiz
if __name__ == "__main__":
    init_db()

