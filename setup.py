from setuptools import setup, find_packages

setup(
    name="juvaana-analytics",
    version="0.1.1",
    author="Juvaana Team",
    description="Interactive EDA + Visualization + HTML reporting library",
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