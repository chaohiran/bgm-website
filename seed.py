from database import get_db

db = get_db()

# =========================
# CATEGORIES
# =========================
categories = [
    ("cat_safety", "Safety"),
    ("cat_automation", "Automation"),
    ("cat_control", "Control"),
    ("cat_lighting", "Lighting"),
    ("cat_switch", "Switch"),
    ("cat_teco", "TECO"),
]

db.executemany(
    "INSERT OR IGNORE INTO categories (key, name) VALUES (?, ?)",
    categories
)

# =========================
# PRODUCTS (6 ตัวของคุณ)
# =========================
products = [
    ("explosion-proof-alarm", "p1_name", "cat_safety", "p1_short", "p1.jpg"),
    ("industrial-automation-system", "p2_name", "cat_automation", "p2_short", "p2.jpg"),
    ("motor-control-panel", "p3_name", "cat_control", "p3_short", "p3.jpg"),
    ("industrial-led-light", "p4_name", "cat_lighting", "p4_short", "p4.jpg"),
    ("emergency-stop-switch", "p5_name", "cat_switch", "p5_short", "p5.jpg"),
    ("teco-inverter-drive", "p6_name", "cat_teco", "p6_short", "p6.jpg"),
]

db.executemany("""
INSERT OR IGNORE INTO products
(slug, name_key, category_key, short_key, image)
VALUES (?, ?, ?, ?, ?)
""", products)

db.commit()
db.close()

print("Seed completed 🚀")