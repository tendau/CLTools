from setuptools import setup, find_packages

setup(
    name="taskcli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "cltasks=cl_tasks.cli:app",
        ],
    },
)
