from setuptools import Extension, find_packages, setup

setup(
    name="cowboy-client",
    version="0.0.9",
    packages=find_packages(),
    description="Cowboy Client Interface",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="John Peng",
    author_email="kongyijipeng@gmail.com",
    install_requires=[
        "click",
        "pyyaml",
        "pydantic",
        "gitpython==3.0.6",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "cowboy = cowboy.cli:entry_point",
        ],
    },
    python_requires=">=3.8",
)
