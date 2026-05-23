import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "bgm.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# เพิ่มฟังก์ชันนี้เข้าไปเพื่อแก้ปัญหา ImportError
def get_company_profile():
    conn = get_db()
    cursor = conn.cursor()
    try:
        # สมมติว่าตารางชื่อ company_profile และดึงข้อมูลแถวแรกมาใช้
        cursor.execute("SELECT * FROM company_profile LIMIT 1")
        profile = cursor.fetchone()
        return profile
    except sqlite3.OperationalError:
        # กันเหนียวไว้: ถ้ายังไม่มีตารางนี้ในฐานข้อมูล ให้คืนค่า None กลับไปก่อน โปรแกรมจะได้ไม่พัง
        return None
    finally:
        conn.close()