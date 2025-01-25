from setuptools import setup, find_packages

setup(
    name="TripoSR",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",           # PyTorch
        "torchmcubes",     # Dependency for 3D model processing
        "flask",           # Flask for building the API
        "flask-cors",      # Handling CORS for Flask API
        "numpy",           # Numerical computations
        "onnxruntime",     # ONNX for AI model execution
        "rembg",           # Background removal (as inferred)
    ],
)
