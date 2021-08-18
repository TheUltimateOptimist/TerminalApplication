from flask import Flask,jsonify
import sql
import functions
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    showOperation = False
    return jsonify({"number": str(sql.execute("SELECT lastname From mitmenschen WHERE firstname = 'Jonathan'", showOperation)[0][0])})


@app.route("/sql/<string:sqloperation>", methods = ["GET"])
def operate(sqloperation):
    result = sql.execute(sqloperation, True)
    result = functions.toStringList(2, result)
    import json
    return jsonify(value=json.dumps(result))    



if __name__ == '__main__':
    app.run(debug=True)