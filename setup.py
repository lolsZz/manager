"""Setup configuration for onhax project."""
from setuptools import setup, find_packages

setup(
    name="onhax",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "onhax=onhax.__main__:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for generating code using DeepSeek API",
    keywords="code generation, ai, deepseek",
    python_requires=">=3.7",
)