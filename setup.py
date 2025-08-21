from setuptools import setup, find_packages

setup(
    name="cognitive_eval",
    version="0.1.0",
    description="Adaptive cognitive evaluation system backend modules",
    author="Youssef Achehboune",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "sentence-transformers",
        "faiss-cpu"
    ],
)