from flask import Flask, request, jsonify
import uuid
import os


def create_app():

    app = Flask(__name__)

    orders = {}

    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV = os.getenv("APP_ENV", "dev")

    @app.route("/")
    def home():
        return jsonify({
            "message": "Restaurant Orders API"
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "UP"
        }), 200

    @app.route("/version")
    def version():
        return jsonify({
            "version": APP_VERSION,
            "environment": APP_ENV
        })

    @app.route("/orders", methods=["POST"])
    def create_order():

        data = request.json

        order_id = str(uuid.uuid4())

        order = {
            "orderId": order_id,
            "customer": data.get("customer"),
            "items": data.get("items"),
            "status": "CREATED"
        }

        orders[order_id] = order

        return jsonify(order), 201

    @app.route("/orders/<order_id>", methods=["GET"])
    def get_order(order_id):

        order = orders.get(order_id)

        if not order:
            return jsonify({
                "error": "Order not found"
            }), 404

        return jsonify(order)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
