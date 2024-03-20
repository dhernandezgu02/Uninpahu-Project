from flask import Flask, request, jsonify, render_template
import networkx as nx
from utils import ruta_mas_corta, G
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},
     origins=['https://u-map.juanses-dev.com/app.html', 'localhost'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular_ruta', methods=['POST'])
def calcular_ruta():
    data = request.get_json()
    if 'origen' not in data or 'destino' not in data:
        return jsonify({"error": "Se requieren nodos de origen y destino"}), 400

    origen = data['origen']
    destino = data['destino']

    try:
        ruta = ruta_mas_corta(G, origen, destino)

        respuesta = {
            "origen": origen,
            "destino": destino,
            "ruta_mas_corta": ruta
        }

        return jsonify(respuesta)

    except nx.NetworkXNoPath:
        return jsonify({"error": "No hay ruta disponible entre los nodos proporcionados"}), 404


if __name__ == '__main__':
    app.run(debug=True)
