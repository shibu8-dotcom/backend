from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
CORS(app)

# -------------------------
# Temporary order storage
# -------------------------
orders = []

# -------------------------
# Home route (already working)
# -------------------------
@app.route("/")
def home():
    return "Smart restaurant is running"

# -------------------------
# Place order (FROM CUSTOMER)
# -------------------------
@app.route("/api/place-order", methods=["POST"])
def place_order():
    data = request.json

    order = {
        "id": len(orders) + 1,
        "table": data.get("table"),
        "items": data.get("items"),
        "total": data.get("total"),
        "status": "Pending",
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    }

    orders.append(order)

    return jsonify({
        "success": True,
        "message": "Order received",
        "order_id": order["id"]
    })

# -------------------------
# Admin: View all orders
# -------------------------
@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

# -------------------------
# Render PORT (VERY IMPORTANT)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
