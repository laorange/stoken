from setuptools import setup, find_packages

from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="stoken",
    version="0.1.3",
    keywords=["git", "data desensitization", "replace token"],
    description="A code desensitization tool, which can substitute tokens (and other sensitive information) in your code.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    url="https://github.com/laorange/stoken",
    project_urls={
        "Bug Tracker": "https://github.com/laorange/stoken/issues",
        "Source Code": "https://github.com/laorange/stoken",
    },
    author="laorange",
    author_email="laorange6666@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pyyaml>=6.0",
        "setuptools>=65.5.0",
        "colorama>=0.4.6",
        "pydantic>=1.10.2",
        "click>=8.1.3",
        "GitPython>=3.1.29",
    ],
    entry_points={
        "console_scripts": [
            "stoken=stoken.main:main"
        ]
    }
)
