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
    description="An AsyncIO asynchronous wrapper around paho-mqtt.",
    license="GPLv2",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="mqtt async asyncio wrapper paho-mqtt",

    # Requirements
    install_requires=["paho-mqtt>=1.3.0"],
)
