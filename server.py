# Save as server.py
from flask import Flask, request, jsonify

API_SECRET_KEY = "8hJk2vX1pQw3rT5s6uV7yZ9aBcDeFgHiJkLmNoPqRsTuVwXyZ"

app = Flask(__name__)

# In-memory license store for demo. Use a database for production!
licenses = {
    "72DP5AP55PZH187S": None,  # Not activated yet
    "WXYZ8765IJKL4321": None,
    "ABCD1234EFGH5678": None,
    "EFGH5678IJKL1234": None,
    "IJKL4321MNOP5678": None,
    "MNOP5678QRST1234": None,
    "QRST1234UVWX5678": None,
    "UVWX5678YZAB1234": None,
    "YZAB1234CDEF5678": None,
    "CDEF5678GHIK1234": None,
    "GHIK1234LMNO5678": None,
    "LMNO5678PQRS1234": None,
    "PQRS1234TUVW5678": None,
    "TUVW5678XYZA1234": None,
    "XYZA1234BCDE5678": None,
    "BCDE5678FGHI1234": None,
    # Add more valid license keys here
}

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    license_key = data.get('license_key')
    device_id = data.get('device_id')
    api_secret = data.get('api_secret')
    
    if api_secret != API_SECRET_KEY:
        return jsonify({"valid": False, "error": "Invalid API secret"}), 403

    if not license_key or not device_id:
        return jsonify({"success": False, "error": "Missing data"}), 400

    if license_key not in licenses:
        return jsonify({"success": False, "error": "Invalid license"}), 400

    if licenses[license_key] is None:
        licenses[license_key] = device_id
        return jsonify({"success": True, "message": "Activated"})
    elif licenses[license_key] == device_id:
        return jsonify({"success": True, "message": "Already activated on this device"})
    else:
        return jsonify({"success": False, "error": "License already used on another device"}), 403

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"success": True, "licenses": licenses})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
