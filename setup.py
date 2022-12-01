from setuptools import setup, find_packages

from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

with open("./requirements.txt", encoding="utf-8") as f:
    install_requires = f.readline()

setup(
    name="stoken",
    version="0.0.1",
    keywords=["git", "data desensitization", "replace token"],
    description="A code desensitization command tool to substitute tokens (and other sensitive information) in your code.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    url="https://github.com/laorange/stoken",
    author="laorange",
    author_email="laorange6666@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires
)
