import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="partenaire-qualif",
    version="0.0.4",
    author="Yanchao MURONG",
    author_email="yanchao.murong@gmail.com",
    description="A simple tool that automates the qualification of a partner(reseller/integrator/editor) by finding its website, industries, business functions and services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ymurong/partenaire-qualif.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'openai>=1.26.0',
        'pandas>=2.2.2',
        'httpx>=0.27.0',
        'validators>=0.28.1',
        'beautifulsoup4>=4.12.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
