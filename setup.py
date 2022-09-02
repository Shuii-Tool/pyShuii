import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pyshuii",
    version="0.0.5",
    description="Multi-chain NFT metadata aggregator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shuii-Tool",
    author="prmali",
    classifiers=[
    ],
    keywords="nft, nfts, shuii, metadata, aggregator, rarity",
    package_dir={"pyshuii": "pyshuii"},
    packages=find_packages(include=["pyshuii*"]),
    python_requires=">=3.6, <4",
    install_requires=[
        "cosmpy",
        "web3",
        "asyncio",
        "aiohttp",
    ],
    extras_require={
        "dev": [
        ],
        "test": [],
    },
    project_urls={
    },
)
