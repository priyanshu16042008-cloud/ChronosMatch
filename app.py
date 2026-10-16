
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample dashboard data
orders = [
    {
        "id": "ORD-10029",
        "symbol": "CMX/USD",
        "side": "BUY",
        "quantity": 100,
        "price": 184.20,
        "status": "PENDING",
        "time": "14:27:12"
    },
    {
        "id": "ORD-10028",
        "symbol": "NOVA/USD",
        "side": "SELL",
        "quantity": 50,
        "price": 72.45,
        "status": "MATCHED",
        "time": "14:26:58"
    },
    {
        "id": "ORD-10027",
        "symbol": "ETH/USD",
        "side": "BUY",
        "quantity": 75,
        "price": 3520.10,
        "status": "PARTIAL",
        "time": "14:26:34"
    }
]

trades = [
    {
        "id": "TRD-50021",
        "symbol": "CMX/USD",
        "side": "BUY",
        "quantity": 100,
        "price": 184.20,
        "time": "14:26:58"
    }
]


@app.route("/")
def dashboard():
    pending_count = sum(
        order["status"] in ("PENDING", "PARTIAL")
        for order in orders
    )

    return render_template(
        "index.html",
        orders=orders,
        trades=trades,
        total_orders=len(orders),
        matched_trades=len(trades),
        pending_orders=pending_count,
        current_time=datetime.now().strftime("%H:%M:%S")
    )


@app.route("/api/orders")
def get_orders():
    return jsonify(orders)


@app.route("/api/trades")
def get_trades():
    return jsonify(trades)


@app.route("/api/order", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    try:
        symbol = data["symbol"]
        side = str(data["side"]).upper()
        quantity = int(data["quantity"])
        price = float(data["price"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid order details"}), 400

    if symbol not in ("CMX/USD", "NOVA/USD", "ETH/USD"):
        return jsonify({"error": "Invalid trading pair"}), 400

    if side not in ("BUY", "SELL"):
        return jsonify({"error": "Invalid order side"}), 400

    if quantity <= 0 or price <= 0:
        return jsonify({"error": "Quantity and price must be positive"}), 400

    order = {
        "id": f"ORD-{10030 + len(orders)}",
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "price": price,
        "status": "PENDING",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    orders.insert(0, order)

    return jsonify({
        "message": "Order submitted successfully",
        "order": order
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
