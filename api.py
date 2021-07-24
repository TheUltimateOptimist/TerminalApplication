from flask import Flask,jsonify
import sql

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    showOperation = False
    return jsonify({"number": str(sql.execute("SELECT lastname From mitmenschen WHERE firstname = 'Jonathan'", showOperation)[0][0])})

if __name__ == '__main__':
    app.run(debug=True)