from flask import Flask, jsonify
from flask import send_from_directory

app = Flask(__name__)


@app.route("/version")
def GET():
    f = open("database", 'r')
    data = []
    for line in f:
        splitline = line.split(',')
        dataline = []
        dataline.append(splitline[0])
        dataline.append(splitline[1])

        data.append(dataline)
    return jsonify(data)

@app.route("/<charts>", methods=['GET'])
def download(charts):

    try:
        return send_from_directory(directory=charts, filename=charts+'.jpeg')
    except Exception, e:
        return(str(e))

if __name__  == "__main__":
    app.run(host='0.0.0.0')
