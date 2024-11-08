from flask import Flask

print("Starting minimal Flask app...")  # Debugging message

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Gigalixir!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 4000))
    print(f"Running minimal app on port {port}...")  # Debugging message
    app.run(host="0.0.0.0", port=port)
