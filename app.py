from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, Response
import openai

app = Flask(__name__)

try:
    @app.route('/')
    def home():
        return render_template("landing.html")

    @app.route('/about')
    def about():
        return render_template("about.html")
    
except Exception as e:
    print(e)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
