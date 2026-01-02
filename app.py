from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Allow ONLY your frontend
CORS(app, origins=[
    "https://violet-justina-31.tiiny.site"
])

DB_NAME = "database.db"


# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_no TEXT,
            items TEXT,
            total INTEGER,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------- API ----------
@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.json

    table_no = data.get("table")
    items = data.get("items")
    total = data.get("total")

    if not table_no or not items:
        return jsonify({"error": "Invalid order"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (table_no, items, total, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        table_no,
        str(items),
        total,
        "PENDING",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    return jsonify({"message": "Order placed successfully"}), 201


@app.route("/api/orders", methods=["GET"])
def get_orders():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        orders.append(dict(row))

    return jsonify(orders)


@app.route("/api/order/status", methods=["POST"])
def update_status():
    data = request.json
    order_id = data.get("id")
    status = data.get("status")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status, order_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated"})


@app.route("/")
def home():
    return "Smart Restaurant Backend Running 🚀"


if __name__ == "__main__":

    app.run(host="0.0.0.0",
    port=int(os.environ.get("PORT".5000)))
