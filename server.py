# Save as server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory license store for demo. Use a database for production!
licenses = {
    "ABCD1234EFGH5678": None,  # Not activated yet
    "WXYZ8765IJKL4321": None,
    # Add more valid license keys here
}

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    license_key = data.get('license_key')
    device_id = data.get('device_id')
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