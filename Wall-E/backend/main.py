from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from test_email import send_alert_email, send_email_notification
import sqlite3
import os

# 📌 FastAPI ilovasini yaratish
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📌 API yaratish
app = FastAPI()

# 📌 Ma'lumotlar bazasi manzili
DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "containers.db")

# 📌 Agar "data" papkasi mavjud bo'lmasa, yaratamiz
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# 📌 Ma'lumotlar bazasiga ulanish
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 📌 Konteyner modeli (GET requestlar uchun)
class Container(BaseModel):
    id: int
    name: str
    weight: float
    max_weight: float
    lat: float
    lon: float

# 📌 Yangi konteyner yaratish uchun model (POST request)
class ContainerCreate(BaseModel):
    name: str
    weight: float
    max_weight: float
    lat: float
    lon: float

# 📌 Barcha konteynerlarni olish
@app.get("/api/containers/", response_model=List[Container])
def get_containers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM containers")
    containers = cursor.fetchall()
    conn.close()
    return [dict(c) for c in containers]
@app.get("/")
def home():
    return {"message": "Wall-E Backend API is running! 🚀"}

# 📌 Yangi konteyner qo‘shish
@app.post("/api/containers/")
def add_container(container: ContainerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO containers (name, weight, max_weight, lat, lon) VALUES (?, ?, ?, ?, ?)",
        (container.name, container.weight, container.max_weight, container.lat, container.lon),
    )
    conn.commit()
    conn.close()

    # 🚨 **Agar konteyner to‘lib ketgan bo‘lsa, email yuboramiz**
    if container.weight >= container.max_weight:
        send_email_notification(
            "🚨 The container is full!",
            f"{container.name} konteyneri {container.weight}/{container.max_weight} kg bo‘lib, to‘lib ketgan!",
            "iskandarovasilbek70@gmail.com",  # Shu yerga emailni qo‘shing
        )

    return {"message": "✅ A new container has been added!"}

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

# 📌 Dastur ishga tushganda, ma’lumotlar bazasini tekshirish
@app.on_event("startup")
def startup():
    init_db()


