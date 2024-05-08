from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ttq",
    version="1.0.0",
    author="Diyorbek Jumanov",
    author_email="djumanovdev@email.com",
    description="Formatlangan matndan testlarni yaratish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djumanov/ttq",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
