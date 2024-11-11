"""
Package configuration.
"""

from setuptools import find_namespace_packages, setup

setup(
    name="recall-space-benchmarks",
    version="0.0.2",
    author="Recall Space",
    author_email="info@recall.space",  
    description="The benchmark package allows you to test AI Brain",
    url="https://github.com/Recall-Space/recall-space-benchmarks",  
    packages=find_namespace_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "pymongo==4.10.1",
        "langchain-cohere",
        "langchain-mistralai",
        "langchain-community",
        "agent-builder"
    ],
    test_suite="tests",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.10",
    ],
)