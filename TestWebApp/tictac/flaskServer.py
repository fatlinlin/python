import os
import json
import tic
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
app.debug = True



grid = tic.Grid()

@app.route("/css/<file>")
def serveCss(file):
    with open(os.path.join("css", file)) as fp:
        return fp.read()

@app.route("/js/<file>")
def serveJs(file):
    with open(os.path.join("js", file)) as fp:
        return fp.read()

@app.route("/<file>")
def serveRootFile(file):
    if file == u'favicon.ico':
        return ""
    with open(file) as fp:
        return fp.read()

@app.route("/tictactoe")
def tictactoe():
   return serveRootFile("tictactoe.html")

@app.route("/")
def index():
    return serveRootFile("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    grid.reset()
    return jsonify()

@app.route("/play/<box>", methods=['POST'])
def play(box):
    print request.args.keys()
    if not grid.isfree(box):
        return jsonify(status = "can't play {}".format(box), grid = grid.grid)

    grid.play(box, "x")
    status = grid.check_status()
    if status != "continue":
        return jsonify(status = status, grid = grid.grid)

    tic.play(grid)
    status = grid.check_status()
    return jsonify(
            status = status,
            grid = grid.grid
            )

if __name__ == "__main__":
    app.run()
