from flask import Flask, jsonify
from flask import send_from_directory

app = Flask(__name__)


@app.route("/version", methods=['GET'])
def database():
    try:
        return send_from_directory(filename="database")
    except Exception, e:
        return(str(e))

@app.route("/<charts>", methods=['GET'])
def download(charts):

    try:
        return send_from_directory(directory=charts, filename=charts+'.jpeg')
    except Exception, e:
        return(str(e))

if __name__  == "__main__":
    app.run(host='0.0.0.0')
