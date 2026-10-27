
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime

from matching_engine import MatchingEngine
from order import Order

app = Flask(__name__)

# One shared matching engine
engine = MatchingEngine()

# Store original order details for dashboard display
orders = []
order_details = {}
trade_details = []

next_order_id = 10030


def get_order_status(order_id):
    """Determine order status from its original and remaining quantity."""
    details = order_details[order_id]
    original_quantity = details["original_quantity"]
    remaining_quantity = details["engine_order"].quantity

    if remaining_quantity == 0:
        return "MATCHED"

    if remaining_quantity < original_quantity:
        return "PARTIAL"

    return "PENDING"


def sync_dashboard_data():
    """Update dashboard orders and trades from the matching engine."""
    global orders, trade_details

    orders = []

    # Display newest orders first.
    for order_id, details in sorted(
        order_details.items(),
        reverse=True
    ):
        engine_order = details["engine_order"]

        orders.append({
            "id": f"ORD-{order_id}",
            "symbol": engine_order.symbol,
            "side": engine_order.side,
            "quantity": engine_order.quantity,
            "original_quantity": details["original_quantity"],
            "price": engine_order.price,
            "status": get_order_status(order_id),
            "time": details["time"]
        })

    # Enrich actual executions for the dashboard.
    trade_details = []

    for index, trade in enumerate(engine.trades, start=1):
        buy_id = trade["buy_order_id"]
        sell_id = trade["sell_order_id"]

        buy_details = order_details[buy_id]

        trade_details.append({
            "id": f"TRD-{index:05d}",
            "buy_order_id": f"ORD-{buy_id}",
            "sell_order_id": f"ORD-{sell_id}",
            "symbol": trade["symbol"],
            "side": "BUY",
            "quantity": trade["quantity"],
            "price": trade["price"],
            "time": buy_details["time"]
        })


@app.route("/")
def dashboard():
    sync_dashboard_data()

    pending_count = sum(
        order["status"] in ("PENDING", "PARTIAL")
        for order in orders
    )

    return render_template(
        "index.html",
        orders=orders,
        trades=trade_details,
        total_orders=len(orders),
        matched_trades=len(trade_details),
        pending_orders=pending_count,
        current_time=datetime.now().strftime("%H:%M:%S")
    )


@app.route("/api/orders")
def get_orders():
    sync_dashboard_data()
    return jsonify(orders)


@app.route("/api/trades")
def get_trades():
    sync_dashboard_data()
    return jsonify(trade_details)


@app.route("/api/order", methods=["POST"])
def create_order():
    global next_order_id

    data = request.get_json(silent=True)

    # Support both JSON requests and standard HTML forms.
    if data is None:
        data = request.form

    try:
        symbol = str(data["symbol"]).strip().upper()
        side = str(data["side"]).strip().upper()
        quantity = int(data["quantity"])
        price = float(data["price"])

        if symbol not in ("CMX/USD", "NOVA/USD", "ETH/USD"):
            raise ValueError("Invalid trading pair")

        # Reject fractional quantities and non-positive values.
        if str(data["quantity"]).strip() != str(quantity):
            raise ValueError("Quantity must be a whole number")

        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        new_order = Order(
            order_id=next_order_id,
            side=side,
            price=price,
            quantity=quantity,
            symbol=symbol
        )

        created_at = datetime.now().strftime("%H:%M:%S")

        order_details[next_order_id] = {
            "symbol": symbol,
            "original_quantity": quantity,
            "time": created_at,
            "engine_order": new_order
        }

        engine.add_order(new_order)
        engine.match_orders()

        submitted_id = next_order_id
        next_order_id += 1

        sync_dashboard_data()

        submitted_order = next(
            item for item in orders
            if item["id"] == f"ORD-{submitted_id}"
        )

        if request.is_json:
            return jsonify({
                "message": "Order processed by matching engine",
                "order": submitted_order,
                "trades": trade_details
            }), 201

        return redirect(url_for("dashboard"))

    except (KeyError, TypeError, ValueError, OverflowError) as error:
        message = str(error) or "Invalid order details"

        if request.is_json:
            return jsonify({"error": message}), 400

        return message, 400


if __name__ == "__main__":
    app.run(debug=True)
