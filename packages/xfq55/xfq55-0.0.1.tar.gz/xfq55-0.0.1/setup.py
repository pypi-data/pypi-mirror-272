import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xfq55",
    version="0.0.1",
    py_modules=["xfq5"],
    author="zcber1",
    author_email="2952964393z@gmail.com",
    description="A simple exe to show stock infos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcber1/xfq5",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests', 'pandas'
    ],
    project_urls={
        'Source': "https://github.com/zcber1/xfq5",
    }
)