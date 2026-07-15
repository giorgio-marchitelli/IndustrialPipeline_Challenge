from flask import Flask, jsonify, request

import database

app = Flask(__name__) # oggetto applicazione Flask 

# la connessione viene passata da main.py dopo aver avviato Flask
connessione_db = None


def imposta_connessione(connessione):
    global connessione_db #globale
    connessione_db = connessione


@app.route("/eventi", methods=["GET"])
def get_eventi():
    limite = request.args.get("limite", default=100, type=int)
    eventi = database.leggi_eventi(connessione_db, limite)
    return jsonify(eventi)


@app.route("/eventi/<int:id_macchina>", methods=["GET"])
def get_eventi_macchina(id_macchina):
    limite = request.args.get("limite", default=100, type=int)
    eventi = database.leggi_eventi_per_macchina(connessione_db, id_macchina, limite)
    return jsonify(eventi)