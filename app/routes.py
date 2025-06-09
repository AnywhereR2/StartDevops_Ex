from flask import request, Response, jsonify
from .models import fetch_all_results, insert_result
import json


def register_routes(app):
    @app.route('/ping')
    def ping():
        return jsonify({"status": "ok"})

    @app.route('/submit', methods=['POST'])
    def submit():
        data = request.get_json()
        if not data or 'name' not in data or 'score' not in data:
            return _resp(400, {"error": "Missing 'name' or 'score'"})
        try:
            insert_result(data['name'], int(data['score']))
            return _resp(200, {"message": "Saved"})
        except Exception as e:
            return _resp(500, {"error": str(e)})

    @app.route('/results', methods=['GET'])
    def results():
        try:
            data = fetch_all_results()
            return _resp(200, {"results": data}, indent=2)
        except Exception as e:
            return _resp(500, {"error": str(e)})

    @app.errorhandler(404)
    def not_found(error):
        return _resp(404, {"error": "Bad endpoint"})


def _resp(code, data, indent=None):
    return Response(
        status=code,
        mimetype="application/json",
        response=json.dumps(data, default=str, indent=indent) + "\n"
    )
