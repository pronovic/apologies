import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apologies",
    version="0.1.0",
    author="Kenneth J. Pronovici",
    author_email="pronovic@ieee.org",
    description="Python code to play a game similar to Sorry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pronovic/apologies",
    python_requires='>=3.7',
    packages=setuptools.find_packages(where='src'),
    scripts=[ 'scripts/apologies' ]
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers", 
        "Natural Language :: English",
        "Topic :: Games/Entertainment :: Board Games", 
        "Topic :: Software Development :: Libraries",
    ],
)
