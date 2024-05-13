from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Text_sentiment_ai_sdk",
    version="1.0.1",
    author="Abdulrafiu Izuafa",
    author_email="izuafa123abdulrafiu@gmail.com",
    description="A Python SDK for AI Text sentiment analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ramseyxlil/Text_Sentiment_analysis",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
)
