from flask import Flask, jsonify, request
app = Flask(__name__)

AUTH_TOKEN='totalsecuretoken123'
AUTH_TOKEN_HEADER_KEY='token'

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify(status='healthy'), 200


@app.route('/closestTop', methods=['GET'])
def closestTop():
    if request.headers.get(AUTH_TOKEN_HEADER_KEY) != AUTH_TOKEN:
        return jsonify(error='failed to authenticate'), 403
    # Hardcoded for testing purposes
    return jsonify(latitude='27.9881', longitude='86.9250'), 200

if __name__ == '__main__':
    app.run()
