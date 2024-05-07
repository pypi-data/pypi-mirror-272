from setuptools import setup, find_packages

setup(
    name="composo",
    version="0.1.37", # ALSO UPDATE IN __init__.py, DO YOU NEED TO UPDATE MINIMUM SUPPORTED VERSION IN BACKEND?
    description="Composo Python Package",
    author="Luke Markham",
    author_email="luke@composo.ai",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "colorama>=0.4.4",
        "pydantic<2.0.0,>=1.9.0"
        
    ],
    python_requires=">=3.8",
)
