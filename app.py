from flask import Flask, render_template, request, jsonify
from agent import create_recommendation

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    problem = data.get("problem", "").strip()

    if not problem:
        return jsonify({
            "error": "Please describe the incident."
        }), 400

    try:
        result = create_recommendation(problem)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)