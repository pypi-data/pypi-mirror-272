import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    installation_requirements = fr.readlines()

setuptools.setup(
    name="pyqflow",
    version="1.1.1",
    author="Goncalo Faria, Guilherme Viveiros, Rui Reis.",
    author_email="goncalo.faria@dotmoovs.com, guilherme.viveiros@dotmoovs.com, rui.reis@dotmoovs.com",
    description="API for creating async workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dotmoovs/remote-workflows-api",
    packages=setuptools.find_packages(),
    install_requires=installation_requirements,
    python_requires=">=3.7.10",
)
