import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dmarc",
    version="1.1.0",
    author="Dusan Obradovic",
    author_email="dusan@euracks.net",
    description="Parse and evaluate DMARC email authentication policy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://gitlab.com/duobradovic/pydmarc",
    packages=setuptools.find_packages(),
    package_data={"dmarc": ["report/schemas/*.xsd", "tests/report/data/*.xml"]},
    keywords = ['dkim', 'spf', 'dmarc', 'email', 'authentication', 'rfc7489', 'rfc8601'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email :: Mail Transport Agents",
        "Topic :: Communications :: Email :: Filters",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.9',
    extras_require={
        "resolver": ['dnspython'],
        "ar": ['authres'],
        "psl": ['publicsuffix2'],
        "report": ['xmlschema'],
    },
)