from flask import Flask, request, jsonify
import os
import subprocess
import sys

app = Flask(__name__)

BASE_DIR = r"D:\main_project\TripoSR"
EXAMPLES_DIR = os.path.join(BASE_DIR, "examples")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REQUIREMENTS_PATH = r"D:\main_project\TripoSR\requirements.txt"

def are_requirements_installed():
    """Check if the required Python packages are already installed"""
    try:
        # Try importing a package that's in your requirements file (e.g., flask)
        import flask
        return True
    except ImportError:
        return False

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(EXAMPLES_DIR, file.filename)
    file.save(file_path)

    try:
        # Only install requirements if they are not already installed
        if not are_requirements_installed():
            command = f"pip install -r {REQUIREMENTS_PATH}"
            subprocess.run(command, cwd=BASE_DIR, shell=True, check=True)

        # Run the command to generate the 3D model
        command = f"python run.py --output-dir {OUTPUT_DIR} {file_path}"
        subprocess.run(command, cwd=BASE_DIR, shell=True, check=True)

        # Assuming the generated 3D model is saved in OUTPUT_DIR
        generated_model_path = os.path.join(OUTPUT_DIR, "generated_model.obj")

        return jsonify({"message": "3D model generated successfully!", "output": generated_model_path}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to generate 3D model: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
