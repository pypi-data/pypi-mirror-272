from setuptools import setup

readme = open("./README.md", "r")
setup(
    name="encryptedcode",
    python_version="3.12.0",
    version="1.1.3",
    description="This library can be used to encrypt and decrypt passwords using the new L0123 algorithm.",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    author="Leandro Gonzalez Espinosa",
    author_email="lworkgonzalez01@gmail.com",
    packages=["encryptedcode"],
    keywords=["encryptation", "encrypted","encode", "decode", "algorithm", "Leandro Gonzalez Espinosa", "Leandro Gonzalez", "Glez Dev"],
    url="https://github.com/leoGlez01/encrypted-code.git",
    license="MIT",
    include_package_data=True,
)
