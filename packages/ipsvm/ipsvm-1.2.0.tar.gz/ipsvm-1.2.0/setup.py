import os

from setuptools import find_packages, setup


version_py = open(os.path.join(os.path.dirname(__file__), "version.py")).read().strip().split("=")[-1].replace('"', "")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ipsvm",
    version="{ver}".format(ver=version_py),
    description="Machine learning algorithm for detection of interplanetary shock waves",
    url="https://bitbucket.org/raysofspace/ipsvm",
    author="Rays of Space Oy",
    author_email="info@raysofspace.com",
    license="MIT",
    packages=find_packages("src", exclude=["test*"]),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
)
