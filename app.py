from flask import Flask, request, jsonify
import calculator

app = Flask(__name__)


@app.route("/add")
def add():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(result=calculator.add(a, b))


@app.route("/subtract")
def subtract():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(result=calculator.subtract(a, b))


@app.route("/multiply")
def multiply():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify(result=calculator.multiply(a, b))


@app.route("/divide")
def divide():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 1))
    try:
        result = calculator.divide(a, b)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(port=5000)
