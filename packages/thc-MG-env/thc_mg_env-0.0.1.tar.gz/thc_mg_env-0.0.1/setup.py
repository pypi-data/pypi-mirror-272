import setuptools
from pathlib import Path

setuptools.setup(
    name="thc_MG_env",
    version="0.0.1",
    description="model of MGs",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="thc_MG_env*"),
    install_requires=['gym']
)