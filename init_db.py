import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "bgm.db")

# สร้างโฟลเดอร์ data ถ้ายังไม่มี
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# =========================
# CATEGORIES
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
)
""")

# =========================
# PRODUCTS
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name_key TEXT NOT NULL,
    category_key TEXT NOT NULL,
    short_key TEXT,
    image TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized:", DB_PATH)