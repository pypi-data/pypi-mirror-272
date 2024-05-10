"""A setuptools based setup module for AIM Flask.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/MrMayami/AIM
"""

from setuptools import setup, find_packages
import pathlib

# Directory containing the setup.py file
here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="aim_flask",  # Required
    version="1.0.2",  # Required
    scripts=['aim_flask.py'],  # Add your script here
    description="A CLI tool for setting up and managing AIM environments",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://github.com/MrMayami/AIM",  # Optional
    author="Joe Mayami",  # Optional
    author_email="pr.mayami@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="AIM Flask",  # Optional
    packages=find_packages(),  # Required
    python_requires=">=3.7, <4",  # Required
     entry_points={
        'console_scripts': [
            'aim=aim_flask:__main__',
        ],
    },
    install_requires=[],  # Optional
    project_urls={  # Optional
        "GitHub": "https://github.com/MrMayami/AIM",
    },
)
