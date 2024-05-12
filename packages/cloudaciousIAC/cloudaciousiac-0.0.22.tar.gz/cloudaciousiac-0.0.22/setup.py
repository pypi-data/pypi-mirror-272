import os
from setuptools import setup, find_packages
import pathlib


# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# here = pathlib.Path(__file__).parent.resolve()
# long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="cloudaciousIAC",
    version=os.getenv("CI_COMMIT_TAG"),
    description="Cloudacious's object-oriented IaC tooling w/Pulumi. Call our classes all day long!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    readme="README.md",
    url="https://gitlab.com/money-marathon/cloudacious/cloudacious-iac.git",
    author="A. SurfingDoggo",
    author_email="git@surfingdoggo.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="setuptools, development",
    package_dir={"": "src"},
    packages=find_packages(),
    python_requires=">=3.11, <4",
    install_requires=[
        "requests",
        "python-gitlab",
        "boto3",
        "python-dotenv",
        "pulumi",
        "pulumi_aws",
        "pulumi_docker",
    ],
)
