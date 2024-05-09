import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sparklestock", ## 소문자 영단어
    version="0.0.0.2", ##
    author="Seyong Ahn", ## ex) Sunkyeong Lee
    author_email="hiseyong1008@gmail.com", ##
    description="sparkle stock package", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hiseyong", ##
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)