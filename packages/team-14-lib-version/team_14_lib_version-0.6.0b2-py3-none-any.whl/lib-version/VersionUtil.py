from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
class VersionUtil:
    @staticmethod
    @app.route('/lib-version', methods=['GET'])
    def get_version(package_name="team_14_lib_version"):
        try:
            dist = importlib.metadata.distribution(package_name)
            return jsonify(dist.version)
        except importlib.metadata.PackageNotFoundError:
            return f"No package named '{package_name}' found."


if __name__ == '__main__':
    app.run(debug=False)
