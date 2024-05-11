from setuptools import setup, find_packages

setup(
    name="ai-diagnosis",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pytorch==2.1.1",
        "torchvision==0.16.1",
        "torchaudio==2.1.1",
        "pytorch-cuda==11.8",
        "numpy==1.26.0",
        "pandas==2.1.1",
        "seaborn==0.13.2",
        "scipy==1.11.4",
        "matplotlib==3.8.0",
        "scikit-learn==1.3.0",
    ],
    long_description_content_type="text/markdown",
)
