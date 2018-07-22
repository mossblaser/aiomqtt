from setuptools import setup, find_packages

with open("aiomqtt/version.py", "r") as f:
    exec(f.read())

setup(
    name="aiomqtt",
    version=__version__,
    packages=find_packages(),

    # Metadata for PyPi
    url="https://github.com/mossblaser/aiomqtt",
    author="Jonathan Heathcote",
    author_email="mail@jhnet.co.uk",
    description="An AsyncIO asynchronous wrapper around paho-mqtt.",
    license="Eclipse Public License v1.0 / Eclipse Distribution License v1.0",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="mqtt async asyncio wrapper paho-mqtt",

    # Requirements
    install_requires=["paho-mqtt>=1.3.0"],
)
