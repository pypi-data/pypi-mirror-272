from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blockchain_python",
    version="0.0.2",
    packages=find_packages(),
    author="Parth Mahakal",
    description="blockchain-python is a lightweight Python library for implementing blockchain technology. It provides an easy-to-use interface for creating decentralized ledgers with features like secure transactions, immutable ledger, and flexible data storage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)
