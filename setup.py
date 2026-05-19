from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="juvaana-analytics",
    version="0.2.1",
    author="Juvaana Team",
    description="Interactive EDA + Visualization + HTML reporting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "plotly"
    ],
    python_requires=">=3.8",
)