from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="chat",
    description="Chat with ChatGPT in your terminal!",
    version="0.2",
    author="Isak Barbopoulos",
    author_email="isak@xaros.org",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    requires=["python (>=3.9)"],
)
