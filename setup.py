import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.readlines()

setuptools.setup(
    name="Remote pi manager", # Replace with your own username
    version="0.0.1",
    author="Narendra N",
    author_email="narendra.klu9@gmail.com",
    description="A package that helps you with performing tasks on your raspberry pi with Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/narendraklu9/remote-pi-manager",
    packages=setuptools.find_packages(),
    install_requires = REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: Raspbian",
    ],
    python_requires='>=3.6',
)