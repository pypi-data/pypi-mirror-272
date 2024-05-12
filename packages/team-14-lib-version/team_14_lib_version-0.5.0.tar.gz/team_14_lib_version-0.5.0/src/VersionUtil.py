from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
class VersionUtil:
    @staticmethod
    @app.route('/lib-version', methods=['GET'])
    def get_version(url="https://api.github.com/repos/remla2024-team14/lib-version/tags"):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            tags = response.json()

            latest_version = max(tag["name"] for tag in tags)
            with open('../version.txt', 'w') as file:
                file.write(latest_version)
            return jsonify("lib-version: " + latest_version)
        except requests.exceptions.RequestException:  # Handles all requests-related exceptions
            try:
                with open("../version.txt", "r") as file:
                    last_saved_version = file.read().strip()
                    return jsonify("last saved lib-version: " + last_saved_version)
            except FileNotFoundError:
                return jsonify("Error: No saved version found.")


if __name__ == '__main__':
    app.run(debug=False)