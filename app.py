from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, Response
from consultant import *
import asyncio
from send_contract import *
from retrieve_contract import *

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

try:
    @app.route('/')
    def home():
        return render_template("landing.html")

    @app.route('/registration')
    def register():
        return render_template("registration.html")
    
    @app.route('/login')
    def login():
        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/chat")
    def chat_redirect():
        return render_template("chatbot.html")  # just an alias route if you want
    
    @app.route("/contract", methods=["GET", "POST"])
    def contract():
        if request.method == "POST":
            party_a = request.form["party_a"]
            party_b = request.form["party_b"]
            clause = request.form["clause"]
            asyncio.run(send_contract(party_a, party_b, clause))
            return "✅ Contract submitted to blockchain successfully!"
        return render_template("contract.html")
    
    @app.route("/retrieve", methods=["GET", "POST"])
    def retrieve():
        if request.method == "POST":
            party_a = request.form["party_a"]
            party_b = request.form["party_b"]
            try:
                result = asyncio.run(fetch_contract(party_a, party_b))
                if result:
                    return render_template("retrieve.html", result=result)
                else:
                    return render_template("retrieve.html", error="Contract not found.")
            except Exception as e:
                return render_template("retrieve.html", error="Contract not found.")
        return render_template("retrieve.html")


    @app.route("/query", methods=["POST"])
    def handle_query():
        data = request.get_json()
        user_input = data.get("input", "")
        if not user_input:
            return jsonify({"reply": "❌ Empty query."}), 400

        try:
            response = chatbot(inp=user_input)
            return jsonify({"reply": response})
        except Exception as e:
            return jsonify({"reply": f"Error: {str(e)}"}), 500
    
except Exception as e:
    print(e)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
