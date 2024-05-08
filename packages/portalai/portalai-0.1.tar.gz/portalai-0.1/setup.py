from setuptools import setup, find_packages

setup(
    name="portalai",
    version="0.1",
    description="Convert code from one language to another using AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="WolfTheDev",
    author_email="wolfthedev@gmail.com",
    url="https://github.com/WolfTheDev/portal",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "ollama==0.1.9",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "portal = portalai.core:portal",
        ],
    },
)
