from setuptools import setup, find_packages

setup(
    name="cllmcli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "google-generativeai>=0.3.0",
        "python-dotenv>=0.21.0"
    ],
    entry_points={
        "console_scripts": [
            "cllm=cl_llm.cli:app",
        ],
    },
)
